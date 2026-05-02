import customtkinter as ctk

from app.theme_colors import Colors


class SecondaryButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=Colors.INPUT,
            hover_color=Colors.SECONDARY_2,
            text_color=Colors.PRIMARY,
            border_color=Colors.PRIMARY,
            border_width=2,
            corner_radius=8,
            **kwargs,
        )
