import winreg


class RegeditChange:

    def __init__(self, color1, color2):
        self.color1, self.color2 = color1.replace(',',
                                                  ''), color2.replace(',', '')

    def check_color(self, color):
        components = color.split()
        if len(components) != 3:
            return False
        try:
            values = [int(c) for c in components]
            return all(0 <= v <= 255 for v in values)
        except ValueError:
            return False

    def accept_color(self):
        if self.check_color(self.color1) and self.check_color(self.color2):
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Control Panel\Colors", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'Hilight', 0, winreg.REG_SZ, self.color1)
            winreg.SetValueEx(key, 'HotTrackingColor', 0, winreg.REG_SZ,
                              self.color2)
            winreg.CloseKey(key)