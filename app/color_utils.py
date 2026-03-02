from models import RGBColor


class ColorConverter:

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        return RGBColor(r, g, b).hex
