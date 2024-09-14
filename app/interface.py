import customtkinter
import tkinter as tk
from change_selection_color import RegeditChange
regedit_change = RegeditChange()


class App(customtkinter.CTk):
    """The main frame where all the functional widgets of the application are located"""

    def __init__(self):
        super().__init__()
        customtkinter.deactivate_automatic_dpi_awareness()
        self.geometry("500x310")
        self.title("Change selection")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.slider_frame = RGBSliders(self)
        self.slider_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.right_func_frame = AnyFuncFrame(self)
        self.right_func_frame.grid(row=0,
                                   column=0,
                                   padx=10,
                                   pady=(10, 10),
                                   sticky="ne")


class AnyFuncFrame(customtkinter.CTkFrame):
    """The rest of the functional widgets are implemented in this class"""

    def __init__(self, master):
        super().__init__(master)
        self.right_frame = customtkinter.CTkFrame(self, width=125, height=273)
        self.right_frame.grid(row=0, column=0, padx=10, pady=(10, 10))
        self.dark_mode_switch_var = customtkinter.BooleanVar(value=RegeditChange.check_system_theme())
        self.dark_mode_switcher = customtkinter.CTkSwitch(
            self.right_frame,
            command=self.dark_mode,
            text="Dark mode",
            variable=self.dark_mode_switch_var,
            onvalue=True,
            offvalue=False)
        self.dark_mode_switcher.grid(row=0, column=0, padx=10, pady=(10, 20))
        self.outline_frame = tk.Frame(self.right_frame,
                                      width=70,
                                      height=70,
                                      bg=regedit_change.hex_color1)
        self.outline_frame.grid(row=1, column=0, padx=10, pady=(0, 20))
        self.fill_frame = tk.Frame(self.outline_frame,
                                   width=60,
                                   height=60,
                                   bg=regedit_change.hex_color2)
        self.fill_frame.grid(row=0, column=0, padx=10, pady=(10, 10))
        self.status_label = customtkinter.CTkLabel(self.right_frame,
                                                   text="Status",
                                                   anchor="center")
        self.status_label.grid(row=3, column=0, padx=10, pady=(0, 0))
        self.progress = customtkinter.CTkProgressBar(self.right_frame,
                                                     orientation="horizontal",
                                                     width=100,
                                                     indeterminate_speed=5,
                                                     determinate_speed=2.5,
                                                     mode="determinate")
        self.progress.set(0)
        self.progress.grid(row=4, column=0, padx=10, pady=(0, 0))
        self.status_text = customtkinter.CTkLabel(self.right_frame,
                                                  text=None,
                                                  anchor="center")
        self.status_text.grid(row=5, column=0, padx=10, pady=(5, 0))
        self.button = customtkinter.CTkButton(self.right_frame,
                                              command=self.accept_event,
                                              text="Accept",
                                              width=100,
                                              height=30)
        self.button.grid(row=6, column=0, padx=10, pady=(10, 10))

    def dark_mode(self):
        """Function to switch between light and dark mode"""
        if self.dark_mode_switch_var.get():
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def preview_event(self):
        """Preview functionality"""
        self.outline_frame.configure(bg=regedit_change.hex_color1)
        self.outline_frame.grid(row=1, column=0, padx=10, pady=(0, 20))
        self.fill_frame.configure(bg=regedit_change.hex_color2)
        self.fill_frame.grid(row=0, column=0, padx=10, pady=(10, 10))

    def accept_event(self):
        """This function is designed to launch the progressbar and accept parameters from the sliders"""
        regedit_change.accept_color()
        self.progress_event()
        self.status_message()

    def progress_event(self):
        """Setting up the progressbar.
        If everything has changed successfully, then the progressbar is filled completely"""
        if regedit_change.status == "Done!":
            self.progress.set(1)
        else:
            self.progress.configure(mode="indeterminate")
            self.progress.start()

    def status_message(self):
        """This func is designed to understand whether everything has changed successfully"""
        self.status_text.configure(text=regedit_change.status)


class RGBSliders(customtkinter.CTkFrame):
    """This class implements sliders and cells for values from sliders. 
    Just from here we take our values for the fill color of the selection and the outline of the selection"""

    def __init__(self, master):
        super().__init__(master)
        self.sliders_frame = customtkinter.CTkFrame(self)
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=(10, 10))
        rgb1, rgb2 = regedit_change.get_color()
        self.slider_entries = [
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_R", rgb1[0],
             customtkinter.CTkLabel, "R"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_G", rgb1[1],
             customtkinter.CTkLabel, "G"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_B", rgb1[2],
             customtkinter.CTkLabel, "B"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "R", rgb2[0],
             customtkinter.CTkLabel, "R"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "G", rgb2[1],
             customtkinter.CTkLabel, "G"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "B", rgb2[2],
             customtkinter.CTkLabel, "B"),
        ]
        self.first_label = customtkinter.CTkLabel(
            self.sliders_frame, text="Outline of the selection")
        self.first_label.grid(row=0, column=0)
        self.second_label = customtkinter.CTkLabel(self.sliders_frame,
                                                   text="Fill selection")
        self.second_label.grid(row=4, column=0)
        for row, (slider_cls, entry_cls, slider_separator, slider_value,
                  label_cls, slider_color) in enumerate(self.slider_entries,
                                                        start=1):
            if row >= 4:
                row += 1
            entry_var = customtkinter.Variable()
            slider = slider_cls(self.sliders_frame,
                                from_=0,
                                to=255,
                                command=self.create_slider_event(
                                    entry_var, slider_separator),
                                number_of_steps=255)
            slider.set(int(slider_value))
            slider.grid(row=row, column=0, padx=(3, 10), pady=(10, 10))
            label = label_cls(self.sliders_frame, text=slider_color)
            label.grid(row=row, column=1, padx=(0, 10))
            entry = entry_cls(self.sliders_frame,
                              placeholder_text=slider_separator,
                              width=50,
                              textvariable=entry_var,
                              validate="key",
                              validatecommand=(self.register(
                                  self.validate_entry), "%P"))
            entry.insert(0, int(slider.get()))
            entry.bind("<FocusOut>",
                       self.create_entry_event(entry_var, slider))
            entry.bind("<Return>", self.create_entry_event(entry_var, slider))
            entry.grid(row=row, column=2, padx=5, pady=0)
            setattr(self, f"slider_{slider_separator}", slider)
            setattr(self, f"label_{slider_separator}", label)
            setattr(self, f"entry_{slider_separator}", entry)

    def create_slider_event(self, entry_var, separator_preview):
        """Creating an event for the slider. 
        Implements feedback with entry widgets and sets the specified values from the slider. 
        Also adds values for the fill of the selection and the outline of the selection"""

        def slider_event(value):
            """The function in the function is designed to have its own event for each slider"""
            entry_var.set(int(value))
            color1 = self.get_slider_values()[:3]
            color2 = self.get_slider_values()[3:]
            regedit_change.insert(color1, color2)
            self.master.right_func_frame.preview_event()

        return slider_event

    def create_entry_event(self, entry_var, slider):
        """Exactly the same situation as 'create_slider_event'"""

        def entry_event(event):
            value = entry_var.get()
            if value == '':
                value = 0
            slider.set(int(value))
            color1 = self.get_slider_values()[:3]
            color2 = self.get_slider_values()[3:]
            regedit_change.insert(color1, color2)
            regedit_change.rgb_to_hex()

        return entry_event

    def get_slider_values(self):
        """Getting values from all sliders"""
        slider_values = []
        for slider_entry in self.slider_entries:
            slider = getattr(self, f"slider_{slider_entry[2]}")
            value = int(slider.get())
            slider_values.append(str(value))
        return slider_values

    @staticmethod
    def validate_entry(value):
        """Checking and restricting entry widgets. 
        It is intended that the entry widgets have only int values and do not exceed 255 because RGB has a maximum value of 255"""
        try:
            if value == "":
                return True
            int_value = int(value)
            return 0 <= int_value <= 255
        except ValueError:
            return False
