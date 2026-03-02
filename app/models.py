from dataclasses import dataclass, field
from typing import Tuple, Optional
from config import AppConstants


@dataclass(slots=True, frozen=True)
class RGBColor:
    r: int
    g: int
    b: int

    def __post_init__(self):
        for component, name in [(self.r, 'R'), (self.g, 'G'), (self.b, 'B')]:
            if not AppConstants.MIN_RGB <= component <= AppConstants.MAX_RGB:
                raise ValueError(f"{name} must be between 0 and 255, got {component}")

    def __str__(self) -> str:
        return f"{self.r} {self.g} {self.b}"

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    def __len__(self) -> int:
        return AppConstants.RGB_COMPONENTS

    def __getitem__(self, index: int) -> int:
        return (self.r, self.g, self.b)[index]

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @classmethod
    def from_string(cls, rgb_string: str) -> "RGBColor":
        parts = rgb_string.strip().split()
        if len(parts) != AppConstants.RGB_COMPONENTS:
            raise ValueError(f"Invalid RGB string: {rgb_string}")
        return cls(*map(int, parts))

    @classmethod
    def from_hex(cls, hex_color: str) -> "RGBColor":
        hex_clean = hex_color.lstrip('#')
        if len(hex_clean) != 6:
            raise ValueError(f"Invalid HEX color: {hex_color}")
        return cls(
            r=int(hex_clean[0:2], 16),
            g=int(hex_clean[2:4], 16),
            b=int(hex_clean[4:6], 16)
        )


@dataclass(slots=True)
class SelectionColors:
    outline: Optional[RGBColor] = None
    fill: Optional[RGBColor] = None

    def __bool__(self) -> bool:
        return self.outline is not None and self.fill is not None

    def __iter__(self):
        yield self.outline
        yield self.fill

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SelectionColors):
            return NotImplemented
        return self.outline == other.outline and self.fill == other.fill

    def to_registry_format(self) -> Tuple[str, str]:
        if not self:
            raise ValueError("Colors not set")
        return str(self.outline), str(self.fill)

    def to_hex_tuple(self) -> Tuple[str, str]:
        if not self:
            raise ValueError("Colors not set")
        return self.outline.hex, self.fill.hex


@dataclass(slots=True)
class AppState:
    colors: SelectionColors = field(default_factory=SelectionColors)
    status: str = ""
    is_dark_mode: bool = False

    def __repr__(self) -> str:
        return f"AppState(status='{self.status}', dark={self.is_dark_mode})"
