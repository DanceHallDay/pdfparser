from abc import ABC


class IFont(ABC):
    def load_font(self, path: str, *args, **kwargs) -> None:
        """
        Loads by @path a font (ttf or ttf)
        """
        pass

    def get_font_name(self, *args, **kwargs) -> str:
        """
        Returns font name
        """
        pass

    def get_font_type(self, *args, **kwargs) -> str:
        """
        Returns fonts type, one from 'REGULAR', 'BOLD', 'ITALIC', 'BOLD-ITALIC'
        """
        pass
