import customtkinter
from change_selection_color import RegeditChange

# reg_change = RegeditChange()


class LightModButton(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.switch_var = customtkinter.StringVar(value="off")
        self.button = customtkinter.CTkSwitch(self,
                                              command=self.checkbox_event(),
                                              text="Темный режим",
                                              variable=self.switch_var,
                                              onvalue="on",
                                              offvalue="off")
        self.button.grid(row=0, column=0, padx=10, pady=(10, 10))

    def checkbox_event(self):
        print("checkbox toggled, current value:", self.switch_var.get())


class AcceptButton(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.button = customtkinter.CTkButton(
            self,
            # command=reg_change.accept_color(),
            command=...,
            text="Применить")
        self.button.grid(row=0, column=0, padx=0, pady=0)


class RGBSliders(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.sliders_frame = customtkinter.CTkFrame(self)
        self.sliders_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 10),
        )

        self.slider_R = customtkinter.CTkSlider(
            self.sliders_frame,
            from_=0,
            to=255,
            command=lambda value: self.slider_event(value, self.entry_R),
            number_of_steps=255)
        self.slider_R.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.entry_R = customtkinter.CTkEntry(self.sliders_frame,
                                              placeholder_text="R",
                                              width=50,
                                              validate="key",
                                              validatecommand=(self.register(
                                                  self.validate_entry), "%P"))
        self.entry_R.insert(0, int(self.slider_R.get()))
        self.entry_R.bind(
            "<Return>",
            lambda event: self.entry_event(self.entry_R, self.slider_R))
        self.entry_R.grid(row=0, column=1, padx=5, pady=0)

        self.slider_G = customtkinter.CTkSlider(
            self.sliders_frame,
            from_=0,
            to=255,
            command=lambda value: self.slider_event(value, self.entry_G),
            number_of_steps=255)
        self.slider_G.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.entry_G = customtkinter.CTkEntry(self.sliders_frame,
                                              placeholder_text="G",
                                              width=50,
                                              validate="key",
                                              validatecommand=(self.register(
                                                  self.validate_entry), "%P"))
        self.entry_G.insert(0, int(self.slider_G.get()))
        self.entry_G.bind(
            "<Return>",
            lambda event: self.entry_event(self.entry_G, self.slider_G))
        self.entry_G.grid(row=1, column=1, padx=5, pady=0)

        self.slider_B = customtkinter.CTkSlider(
            self.sliders_frame,
            from_=0,
            to=255,
            command=lambda value: self.slider_event(value, self.entry_B),
            number_of_steps=255)
        self.slider_B.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.entry_B = customtkinter.CTkEntry(self.sliders_frame,
                                              placeholder_text="B",
                                              width=50,
                                              validate="key",
                                              validatecommand=(self.register(
                                                  self.validate_entry), "%P"))
        self.entry_B.insert(0, int(self.slider_B.get()))
        self.entry_B.bind(
            "<Return>",
            lambda event: self.entry_event(self.entry_B, self.slider_B))
        self.entry_B.grid(row=2, column=1, padx=5, pady=0)

    @staticmethod
    def slider_event(value, entry):
        entry.delete(0, customtkinter.END)
        entry.insert(0, int(value))

    @staticmethod
    def entry_event(entry, slider):
        value = entry.get()
        slider.set(float(value))

    @staticmethod
    def validate_entry(value):
        try:
            if value == "":
                return True
            int_value = int(value)
            return 0 <= int_value <= 255
        except ValueError:
            return False


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("600x450")
        self.title("Change selection")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.first_label = customtkinter.CTkLabel(self,
                                                  text="Контур выделения")
        self.first_label.grid(row=0, column=0, padx=10, pady=10)

        # self.slider_frame_hilight = RGBSliders(self)
        # self.slider_frame_hilight.grid(row=1,
        #                                column=0,
        #                                padx=10,
        #                                pady=10,
        #                                sticky="nw")
        # self.second_label = customtkinter.CTkLabel(self,
        #                                            text="Заливка выделения")
        # self.first_label.grid(row=2, column=0, sticky="nw")

        # self.slider_frame_hot_tracking_color = RGBSliders(self)
        # self.slider_frame_hot_tracking_color.grid(row=3,
        #                                           column=0,
        #                                           padx=10,
        #                                           pady=10,
        #                                           sticky="nw")

        # self.accept_button = AcceptButton(self)
        # self.accept_button.grid(row=0, column=0, padx=10, pady=10, sticky="se")

        # self.dark_mod_button = LightModButton(self)
        # self.dark_mod_button.grid(row=0,
        #                           column=0,
        #                           padx=10,
        #                           pady=10,
        #                           sticky="ne")


app = App()
app.mainloop()