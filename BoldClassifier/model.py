import torch
from torchvision import models
from torch import nn, Tensor
from einops import rearrange, reduce, repeat
from einops.layers.torch import Rearrange, Reduce
import torch.nn.functional as F

class PatchEmbeddingBlock(nn.Module):
    def __init__(self, feature_extraction_model = None, num_words : int = 8, emb_size : int = 64): 
        super(PatchEmbeddingBlock, self).__init__()
        self.projection = nn.Sequential(
            Rearrange('b n c h w -> (b n) c h w'),# batch_size, num_words, chanels, height, width
            feature_extraction_model if feature_extraction_model is not None else self.__default_FE_model(emb_size), #resnet18
            Rearrange('(b n) e -> b n e', e = emb_size, n = num_words),#batch_size, num_words, emb_size
        )
        self.positions = nn.Parameter(torch.randn(num_words, emb_size))
    
    def __default_FE_model(self, emb_size):
        resnet = models.resnet18(pretrained=True)
        resnet.fc = nn.Linear(512, emb_size) 
        return resnet
    
    def forward(self, x : Tensor) -> Tensor:
        x = self.projection(x)
        x += self.positions
        return x

    
class MultiHeadAttentionBlock(nn.Module):
    def __init__(self, emb_size : int = 64, num_heads : int = 2, dropout : float = 0):
        super(MultiHeadAttentionBlock, self).__init__()
        self.emb_size = emb_size
        self.num_heads = num_heads
        self.dropout = nn.Dropout(dropout)
        self.qkv_linear_layer = nn.Linear(emb_size, emb_size * 3)
        self.projection = nn.Linear(emb_size, emb_size)

    def forward(self, x : Tensor, mask : Tensor = None) -> Tensor:
        queries, keys, values = rearrange(self.qkv_linear_layer(x), 'b n (qkv h d) -> (qkv) b h n d', h=self.num_heads,qkv = 3)
        #computing attention
        sum = torch.einsum('bhqd, bhkd -> bhqk', queries, keys)

        if mask is not None:
            pass
                
        scaling = self.emb_size ** (1/2)
        att = F.softmax(sum, dim=1) / scaling
        att = self.dropout(att)
        out = torch.einsum('bhal, bhlv -> bhav ', att, values)
        #merging
        out = rearrange(out, "b h n d -> b n (h d)")
        out = self.projection(out)
        return out
    
    
class ResBlock(nn.Module):
    def __init__(self, fn):
        super(ResBlock, self).__init__()
        self.fn = fn

    def forward(self, x, **kwargs) -> Tensor:
        residual = x
        x = self.fn(x, **kwargs)
        x += residual
        return x   
    
    
class FeedForwardBlock(nn.Sequential):
    def __init__(self, emb_size : int = 8, expapansion : int = 4, dropout : float = 0):
        super(FeedForwardBlock, self).__init__(
            nn.Linear(emb_size, expapansion * emb_size),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(emb_size * expapansion, emb_size)
        )

class TransformerBlock(nn.Sequential):
    def __init__(self, num_heads : int = 2, emb_size : int = 64, forward_expansion : int = 3, forward_dropout : float = 0, 
                  attention_dropout : float = 0,dropout : float = 0):
        super(TransformerBlock, self).__init__(
            ResBlock(nn.Sequential(
                nn.LayerNorm(emb_size),
                MultiHeadAttentionBlock(emb_size, num_heads, attention_dropout),
                nn.Dropout(dropout),
            )),
            ResBlock(nn.Sequential(
                nn.LayerNorm(emb_size),
                FeedForwardBlock(emb_size, forward_expansion, forward_dropout),
                nn.Dropout(dropout),
            )),
        ) 
       
        
class BoldClassifier(nn.Sequential):
    def __init__(self, feature_extraction_model = None, depth : int = 4, emb_size : int = 64, num_words : int = 8, num_heads : int = 2,  forward_expansion : int = 3, **kwargs):
        super(BoldClassifier, self).__init__(
            PatchEmbeddingBlock(feature_extraction_model, num_words, emb_size),
            *[TransformerBlock(num_heads, emb_size, forward_expansion,**kwargs) for _ in range(depth)],
            nn.Linear(emb_size, 2)
        )    
