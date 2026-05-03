import customtkinter as ctk

from app.theme_colors import Colors


class SecondaryButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=Colors.CARD,
            hover_color=Colors.SURFACE,
            text_color=Colors.TEXT_DARK,
            border_color=Colors.BORDER_LIGHT,
            border_width=1,
            corner_radius=10,
            **kwargs,
        )
