import customtkinter as ctk

from app.theme_colors import Colors


class PrimaryButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color="white",
            corner_radius=10,
            **kwargs,
        )
