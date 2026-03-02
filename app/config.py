from enum import Enum


class RegistryPaths:
    COLORS = r"Control Panel\Colors"
    THEMES = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"

    HILIGHT_KEY = "Hilight"
    HOT_TRACKING_KEY = "HotTrackingColor"
    THEME_KEY = "AppsUseLightTheme"


class AppConstants:
    APP_NAME = "Change Selection Color"
    APP_VERSION = "3.3.4"
    MIN_RGB = 0
    MAX_RGB = 255
    RGB_COMPONENTS = 3

    ICON_FILE = "icon.ico"


class StatusMessages(Enum):
    SUCCESS = "Done!"
    ERROR = "Error!"
    INVALID_COLOR = "Invalid color format!"
    REGISTRY_ERROR = "Registry access error!"


class UIConstants:
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 310
    PREVIEW_SIZE = 90
    PREVIEW_INNER_SIZE = 70
