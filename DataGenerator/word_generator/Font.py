from DataGenerator.word_generator.IFont import IFont
import os

class Font(IFont):
    def load_font(self, path: str, *args, **kwkwargsargs) -> None:
        if not os.path.isfile(path) or not path.lower().endswith('.ttf'):
            raise OSError("only .ttf and .otf fonts can be used")
        self.font = path
        self.name = os.path.basename(self.font)
    
    def get_font_name(self, *args, **kwargs) -> str:
        return self.name

    def get_font_type(self, *args, **kwargs) -> str:
        if 'bold' in self.name and 'italic' in self.name:
            return 'bold-italic'
        elif 'italic' in self.name:
            return 'italic'
        elif 'bold' in self.name:
            return 'bold'
        else:
            return 'regular'
