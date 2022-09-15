from .IFont import IFont
import os

class Font(IFont):
    def load_font(self, path: str, *args, **kwkwargsargs) -> None:
        if not os.path.isfile(path) or not path.lower().endswith('.ttf'):
            raise OSError("only .ttf and .otf fonts can be used")
        self.font = path
    
    def get_font_name(self, *args, **kwargs) -> str:
        return os.path.basename(self.font)

    def get_font_type(self, *args, **kwargs) -> str:
        name = os.path.basename(self.font).lower()
        if 'bold' in name and 'italic' in name:
            return 'bold-italic'
        elif 'italic' in name:
            return 'italic'
        elif 'bold' in name:
            return 'bold'
        else:
            return 'regular'
