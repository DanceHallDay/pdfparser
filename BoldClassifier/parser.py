from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator
from typing import List, Union
from PIL import Image
import fitz
import io
import numpy as np

class PdfParser:
    def parse_pdf(self, pdf_path : str, fonttype : str) -> List[Union[np.array, List[int], str, str]]:
        pdf = open(pdf_path, 'rb')
        words_list = []
        pages_imgs = self.__get_pages_images(pdf_path)
        
        manager = PDFResourceManager()
        laparams = LAParams()
        dev = PDFPageAggregator(manager, laparams=laparams)
        interpreter = PDFPageInterpreter(manager, dev)
        pages = PDFPage.get_pages(pdf)

        for i, page in enumerate(pages):
            interpreter.process_page(page)
            layout = dev.get_result()
            x0, y0, x1, y1, text, font_name = -1, -1, -1, -1, '', ''
            for textbox in layout:
                if isinstance(textbox, LTText):
                    for line in textbox:
                        for char in line:
                          # If the char is a line-break or an empty space, the word is complete
                            if isinstance(char, LTAnno) or char.get_text() == ' ':
                                if x1 != -1:
                                    words_list.append(
                                        [
                                            pages_imgs[i, (pages_imgs.shape[1] - y1):(pages_imgs.shape[1] - y0), x0:x1, :3],
                                            [x0, y0, x1, y1], 
                                            text, 
                                            int(fonttype in font_name.lower())
                                        ]
                                    )
                                    #print('At %r is text: %s' % ((x, y), text))
                                x1, text = -1, ''     
                            elif isinstance(char, LTChar):
                                #print(char.)
                                text += char.get_text()
                                font_name = char.fontname
                                if x1 == -1:
                                    x0, y0, x1, y1 = int(char.x0), int(char.y0), int(char.x1), int(char.y1) 
                                x1 = int(char.x1)
            # If the last symbol in the PDF was neither an empty space nor a LTAnno, print the word here
            if x0 != -1:
                words_list.append(
                    [
                        pages_imgs[i, (pages_imgs[i].shape[1] - y1):(pages_imgs[i].shape[1] - y0), x0:x1, :3],
                        [x0, y0, x1, y1], 
                        text, 
                        int(fonttype in font_name.lower())
                    ]
                )    
                #print('At %r is text: %s' % ((x, y), text))
                    
        return words_list
        
    def __get_pages_images(self, pdf_path: str) -> np.array:
        pages_img = []
        pdf = fitz.open(pdf_path)
        
        for i in range(len(pdf)):
            page = pdf[i] 
            pix = page.get_pixmap()
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples) # from page bitmap to pillow image 
            pages_img.append(np.array(img))
            
        return np.array(pages_img)