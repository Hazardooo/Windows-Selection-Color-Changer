import winreg
import ctypes
from ctypes import wintypes


class RegeditChange:
    """This class is designed to change the values in the register in order to change the selection color"""

    def __init__(self):
        self.rgb_color1, self.rgb_color2 = None, None
        self.hex_color1, self.hex_color2 = None, None
        self.status = None

    def insert(self, color1, color2):
        """Adding our RGB values"""
        self.rgb_color1, self.rgb_color2 = ' '.join(color1), ' '.join(color2)
        self.rgb_to_hex()

    def accept_color(self):
        """We accept our RGB values and enter them in the registry"""
        if self.check_color(self.rgb_color1) and self.check_color(
                self.rgb_color2):
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Control Panel\Colors", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'Hilight', 0, winreg.REG_SZ,
                              self.rgb_color1)
            winreg.SetValueEx(key, 'HotTrackingColor', 0, winreg.REG_SZ,
                              self.rgb_color2)
            winreg.CloseKey(key)
            self.status = "Done!"
            return
        self.status = "Error!"
        return

    def get_color(self):
        """Getting the value from the register"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Colors")
        self.rgb_color1 = winreg.QueryValueEx(key, 'Hilight')[0]
        self.rgb_color2 = winreg.QueryValueEx(key, 'HotTrackingColor')[0]
        winreg.CloseKey(key)
        self.rgb_to_hex()
        return self.rgb_color1.split(), self.rgb_color2.split()

    def rgb_to_hex(self):
        """Convert from RGB to HEX"""
        split_colors1, split_colors2 = self.rgb_color1.split(
        ), self.rgb_color2.split()
        self.hex_color1 = "#{:02x}{:02x}{:02x}".format(int(split_colors1[0]),
                                                       int(split_colors1[1]),
                                                       int(split_colors1[2]))
        self.hex_color2 = "#{:02x}{:02x}{:02x}".format(int(split_colors2[0]),
                                                       int(split_colors2[1]),
                                                       int(split_colors2[2]))

    @staticmethod
    def check_system_theme():
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
            light_theme, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
            winreg.CloseKey(reg_key)
            if light_theme == 0:
                return True
            else:
                return False
        except Exception as e:
            return f"Ошибка при чтении реестра: {e}"

    @staticmethod
    def check_color(color):
        """Checking our RGB values"""
        if color == None:
            return False
        color_split = color.split()
        if len(color_split) != 3:
            return False
        try:
            values = [int(c) for c in color_split]
            return all(0 <= v <= 255 for v in values)
        except ValueError:
            return False
