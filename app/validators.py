from typing import Union, List
from config import AppConstants


class ColorValidator:

    @staticmethod
    def validate_rgb_component(value: Union[str, int]) -> bool:
        try:
            int_val = int(value)
            return AppConstants.MIN_RGB <= int_val <= AppConstants.MAX_RGB
        except (ValueError, TypeError):
            return False

    @classmethod
    def validate_rgb_list(cls, colors: List[Union[str, int]]) -> bool:
        if len(colors) != AppConstants.RGB_COMPONENTS:
            return False
        return all(cls.validate_rgb_component(c) for c in colors)

    @classmethod
    def validate_rgb_string(cls, color_string: str) -> bool:
        if not color_string or not isinstance(color_string, str):
            return False
        parts = color_string.split()
        return cls.validate_rgb_list(parts)

    @staticmethod
    def validate_hex(hex_string: str) -> bool:
        if not hex_string.startswith('#') or len(hex_string) != 7:
            return False
        try:
            int(hex_string[1:], 16)
            return True
        except ValueError:
            return False