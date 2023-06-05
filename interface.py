import customtkinter
from change_selection_color import RegeditChange

regedit_change = RegeditChange()


class Switches(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.light_switch_var = customtkinter.StringVar(value="off")
        self.button = customtkinter.CTkSwitch(
            self,
            #   command=self.checkbox_event(),
            command=...,
            text="Темный режим",
            variable=self.light_switch_var,
            onvalue="on",
            offvalue="off")
        self.button.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")

        self.lang_switch_var = customtkinter.StringVar(value="off")
        self.button = customtkinter.CTkSwitch(
            self,
            command=...,
            #   command=self.checkbox_event(),
            text="RUS/ENG",
            variable=self.lang_switch_var,
            onvalue="on",
            offvalue="off")
        self.button.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="w")


class AcceptButton(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.button = customtkinter.CTkButton(
            self, command=regedit_change.accept_color, text="Применить")
        self.button.grid(row=0, column=0, padx=0, pady=0)


class RGBSliders(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.sliders_frame = customtkinter.CTkFrame(self)
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=(10, 10))

        self.slider_entries = [
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_R"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_G"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "_B"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "R"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "G"),
            (customtkinter.CTkSlider, customtkinter.CTkEntry, "B"),
        ]
        self.first_label = customtkinter.CTkLabel(self.sliders_frame,
                                                  text="Контур выделения")
        self.first_label.grid(row=0, column=0)
        self.second_label = customtkinter.CTkLabel(self.sliders_frame,
                                                   text="Заливка выделения")
        self.second_label.grid(row=4, column=0)
        for row, (slider_cls, entry_cls,
                  text) in enumerate(self.slider_entries, start=1):
            if row >= 4:
                row += 1
            entry_var = customtkinter.Variable()
            slider = slider_cls(self.sliders_frame,
                                from_=0,
                                to=255,
                                command=self.create_slider_event(entry_var),
                                number_of_steps=255)
            slider.grid(row=row, column=0, padx=20, pady=(10, 10))
            entry = entry_cls(self.sliders_frame,
                              placeholder_text=text,
                              width=50,
                              textvariable=entry_var,
                              validate="key",
                              validatecommand=(self.register(
                                  self.validate_entry), "%P"))
            entry.insert(0, int(slider.get()))
            entry.bind("<Return>", self.create_entry_event(entry_var, slider))
            entry.grid(row=row, column=1, padx=5, pady=0)

            setattr(self, f"slider_{text}", slider)
            setattr(self, f"entry_{text}", entry)

    def create_slider_event(self, entry_var):

        def slider_event(value):
            entry_var.set(int(value))
            color1 = self.get_slider_values()[:3]
            color2 = self.get_slider_values()[3:]
            regedit_change.insert(color1, color2)

        return slider_event

    def create_entry_event(self, entry_var, slider):

        def entry_event(event):
            value = entry_var.get()
            if value == '':
                value = 0
            slider.set(int(value))
            color1 = self.get_slider_values()[:3]
            color2 = self.get_slider_values()[3:]
            regedit_change.insert(color1, color2)

        return entry_event

    @staticmethod
    def validate_entry(value):
        try:
            if value == "":
                return True
            int_value = int(value)
            return 0 <= int_value <= 255
        except ValueError:
            return False

    def get_slider_values(self):
        slider_values = []
        for slider_entry in self.slider_entries:
            slider = getattr(self, f"slider_{slider_entry[2]}")
            value = int(slider.get())
            slider_values.append(str(value))
        return slider_values


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("500x310")
        self.title("Change selection")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.slider_frame = RGBSliders(self)
        self.slider_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.accept_button = AcceptButton(self)
        self.accept_button.grid(row=0, column=0, padx=10, pady=10, sticky="se")

        self.dark_mod_button = Switches(self)
        self.dark_mod_button.grid(row=0,
                                  column=0,
                                  padx=10,
                                  pady=10,
                                  sticky="ne")


app = App()
app.mainloop()