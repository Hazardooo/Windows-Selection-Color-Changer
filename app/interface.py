import tkinter as tk
from typing import Callable
from pathlib import Path

import customtkinter

from config import UIConstants, AppConstants
from models import RGBColor, SelectionColors
from registry_service import RegistryService


class ColorController:
    __slots__ = ('_service', '_on_change_callback')

    def __init__(self, on_change: Callable = None):
        self._service = RegistryService()
        self._on_change_callback = on_change

    def load_colors(self) -> SelectionColors:
        return self._service.read_selection_colors()

    def save_colors(self, outline: RGBColor, fill: RGBColor) -> bool:
        colors = SelectionColors(outline=outline, fill=fill)
        success = self._service.write_selection_colors(colors)
        if self._on_change_callback:
            self._on_change_callback(success, self._service.last_status)
        return success

    def get_system_theme(self) -> bool:
        return self._service.check_system_theme()

    @property
    def status(self) -> str:
        return self._service.last_status


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._set_icon()

        self.controller = ColorController(on_change=self._on_colors_changed)
        initial_colors = self.controller.load_colors()

        self.slider_frame = RGBSliders(self, initial_colors, self._on_slider_changed)
        self.slider_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.right_frame = ControlPanel(
            self,
            initial_colors,
            self.controller.get_system_theme(),
            self._on_accept_clicked
        )
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def _setup_window(self):
        customtkinter.deactivate_automatic_dpi_awareness()
        self.geometry(f"{UIConstants.WINDOW_WIDTH}x{UIConstants.WINDOW_HEIGHT}")
        self.title(AppConstants.APP_NAME)
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

    def _set_icon(self):
        try:
            icon_path = Path(AppConstants.ICON_FILE)
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception:
            pass

    def _on_slider_changed(self, outline: RGBColor, fill: RGBColor):
        self.right_frame.update_preview(outline.hex, fill.hex)

    def _on_accept_clicked(self):
        outline, fill = self.slider_frame.get_colors()
        success = self.controller.save_colors(outline, fill)
        self.right_frame.show_status(success, self.controller.status)

    def _on_colors_changed(self, success: bool, status: str):
        pass


class ControlPanel(customtkinter.CTkFrame):
    __slots__ = ('preview_outline', 'preview_fill', 'status_label',
                 'progress_bar', 'status_text', 'dark_switch')

    def __init__(self, master, colors: SelectionColors, is_dark: bool,
                 accept_callback: Callable):
        super().__init__(master)

        self._create_theme_switch(is_dark)
        self._create_preview(colors)
        self._create_status_area()
        self._create_accept_button(accept_callback)

    def _create_theme_switch(self, is_dark: bool):
        self.dark_switch = customtkinter.CTkSwitch(
            self,
            text="Dark mode",
            command=self._toggle_theme,
            variable=customtkinter.BooleanVar(value=is_dark)
        )
        self.dark_switch.grid(row=0, column=0, padx=10, pady=(10, 20))

    def _create_preview(self, colors: SelectionColors):
        outline_hex = colors.outline.hex if colors.outline else "#000000"
        fill_hex = colors.fill.hex if colors.fill else "#000000"

        self.preview_outline = tk.Frame(
            self,
            width=UIConstants.PREVIEW_SIZE,
            height=UIConstants.PREVIEW_SIZE,
            bg=outline_hex
        )
        self.preview_outline.grid(row=1, column=0, padx=10, pady=(0, 20))

        self.preview_fill = tk.Frame(
            self.preview_outline,
            width=UIConstants.PREVIEW_INNER_SIZE,
            height=UIConstants.PREVIEW_INNER_SIZE,
            bg=fill_hex
        )
        self.preview_fill.place(relx=0.5, rely=0.5, anchor="center")

    def _create_status_area(self):
        self.status_label = customtkinter.CTkLabel(self, text="Status")
        self.status_label.grid(row=2, column=0, padx=10)

        self.progress_bar = customtkinter.CTkProgressBar(
            self,
            orientation="horizontal",
            width=100,
            mode="determinate"
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=0, padx=10, pady=(5, 0))

        self.status_text = customtkinter.CTkLabel(self, text="")
        self.status_text.grid(row=4, column=0, padx=10, pady=(5, 0))

    def _create_accept_button(self, callback: Callable):
        btn = customtkinter.CTkButton(
            self,
            text="Accept",
            command=callback,
            width=100,
            height=30
        )
        btn.grid(row=5, column=0, padx=10, pady=(15, 10))

    def _toggle_theme(self):
        mode = "dark" if self.dark_switch.get() else "light"
        customtkinter.set_appearance_mode(mode)

    def update_preview(self, outline_hex: str, fill_hex: str):
        self.preview_outline.configure(bg=outline_hex)
        self.preview_fill.configure(bg=fill_hex)

    def show_status(self, success: bool, message: str):
        self.status_text.configure(text=message)
        if success:
            self.progress_bar.set(1)
            self.progress_bar.configure(progress_color="green")
        else:
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            self.progress_bar.configure(progress_color="red")


class RGBSliders(customtkinter.CTkFrame):
    __slots__ = ('sliders', 'entries', 'labels', '_outline', '_fill')

    def __init__(self, master, colors: SelectionColors, change_callback: Callable):
        super().__init__(master)
        self._on_change = change_callback

        self.sliders = {}
        self.entries = {}
        self.labels = {}

        self._create_headers()
        self._create_sliders(colors)

    def _create_headers(self):
        customtkinter.CTkLabel(self, text="Outline of the selection").grid(
            row=0, column=0, columnspan=3, pady=(0, 5))
        customtkinter.CTkLabel(self, text="Fill selection").grid(
            row=4, column=0, columnspan=3, pady=(15, 5))

    def _create_sliders(self, colors: SelectionColors):
        outline = colors.outline or RGBColor(0, 120, 215)
        fill = colors.fill or RGBColor(0, 120, 215)

        config = [
            ("_R", outline.r, "R"), ("_G", outline.g, "G"), ("_B", outline.b, "B"),
            ("R", fill.r, "R"), ("G", fill.g, "G"), ("B", fill.b, "B")
        ]

        for idx, (name, value, label) in enumerate(config):
            row = idx + 1 if idx < 3 else idx + 2

            slider = customtkinter.CTkSlider(
                self,
                from_=0,
                to=255,
                number_of_steps=255,
                command=lambda v, n=name: self._slider_changed(n, v)
            )
            slider.set(value)
            slider.grid(row=row, column=0, padx=(20, 10), pady=8)

            lbl = customtkinter.CTkLabel(self, text=label, width=20)
            lbl.grid(row=row, column=1, padx=(0, 5))

            entry_var = customtkinter.StringVar(value=str(int(value)))
            entry = customtkinter.CTkEntry(
                self,
                width=50,
                textvariable=entry_var,
                validate="key",
                validatecommand=(self.register(self._validate), "%P")
            )
            entry.bind("<FocusOut>", lambda e, n=name, ev=entry_var: self._entry_changed(n, ev))
            entry.bind("<Return>", lambda e, n=name, ev=entry_var: self._entry_changed(n, ev))
            entry.grid(row=row, column=2, padx=5)

            self.sliders[name] = slider
            self.entries[name] = (entry, entry_var)
            self.labels[name] = lbl

        self._outline = outline
        self._fill = fill

    @staticmethod
    def _validate(value: str) -> bool:
        if value == "":
            return True
        try:
            num = int(value)
            return 0 <= num <= 255
        except ValueError:
            return False

    def _slider_changed(self, name: str, value: float):
        entry, var = self.entries[name]
        var.set(str(int(value)))
        self._update_color(name, int(value))
        self._notify_change()

    def _entry_changed(self, name: str, var: customtkinter.StringVar):
        val = var.get()
        if val == "":
            val = "0"
            var.set(val)

        num = int(val)
        self.sliders[name].set(num)
        self._update_color(name, num)
        self._notify_change()

    def _update_color(self, name: str, value: int):
        if name.startswith("_"):
            current = self._outline
            if name == "_R":
                self._outline = RGBColor(value, current.g, current.b)
            elif name == "_G":
                self._outline = RGBColor(current.r, value, current.b)
            else:
                self._outline = RGBColor(current.r, current.g, value)
        else:
            current = self._fill
            if name == "R":
                self._fill = RGBColor(value, current.g, current.b)
            elif name == "G":
                self._fill = RGBColor(current.r, value, current.b)
            else:
                self._fill = RGBColor(current.r, current.g, value)

    def _notify_change(self):
        self._on_change(self._outline, self._fill)

    def get_colors(self) -> tuple[RGBColor, RGBColor]:
        return self._outline, self._fill
