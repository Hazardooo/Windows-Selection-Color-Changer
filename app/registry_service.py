import winreg
from dataclasses import dataclass

from config import RegistryPaths, StatusMessages
from models import RGBColor, SelectionColors, AppState


@dataclass(slots=True)
class RegistryService:
    _state: AppState = None

    def __post_init__(self):
        if self._state is None:
            self._state = AppState()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def read_selection_colors(self) -> SelectionColors:
        colors = SelectionColors()

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RegistryPaths.COLORS) as key:
                outline_str, _ = winreg.QueryValueEx(key, RegistryPaths.HILIGHT_KEY)
                colors.outline = RGBColor.from_string(outline_str)

                fill_str, _ = winreg.QueryValueEx(key, RegistryPaths.HOT_TRACKING_KEY)
                colors.fill = RGBColor.from_string(fill_str)

                self._state.status = StatusMessages.SUCCESS.value

        except FileNotFoundError:
            self._state.status = "Registry keys not found"
        except PermissionError:
            self._state.status = StatusMessages.REGISTRY_ERROR.value
        except Exception as e:
            self._state.status = f"Error: {str(e)}"

        self._state.colors = colors
        return colors

    def write_selection_colors(self, colors: SelectionColors) -> bool:
        """Запись цветов в реестр"""
        if not colors:
            self._state.status = StatusMessages.INVALID_COLOR.value
            return False

        try:
            with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    RegistryPaths.COLORS,
                    0,
                    winreg.KEY_WRITE
            ) as key:

                outline_str, fill_str = colors.to_registry_format()

                winreg.SetValueEx(key, RegistryPaths.HILIGHT_KEY, 0, winreg.REG_SZ, outline_str)
                winreg.SetValueEx(key, RegistryPaths.HOT_TRACKING_KEY, 0, winreg.REG_SZ, fill_str)

                self._state.status = StatusMessages.SUCCESS.value
                self._state.colors = colors
                return True

        except PermissionError:
            self._state.status = StatusMessages.REGISTRY_ERROR.value
        except Exception as e:
            self._state.status = f"Error: {str(e)}"

        return False

    def check_system_theme(self) -> bool:
        try:
            with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    RegistryPaths.THEMES
            ) as key:
                light_theme, _ = winreg.QueryValueEx(key, RegistryPaths.THEME_KEY)
                self._state.is_dark_mode = (light_theme == 0)
                return self._state.is_dark_mode
        except Exception:
            self._state.is_dark_mode = False
            return False

    @property
    def last_status(self) -> str:
        return self._state.status

    @property
    def current_colors(self) -> SelectionColors:
        return self._state.colors
