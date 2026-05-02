import customtkinter as ctk

from app.theme_colors import Colors


class LinkLabel(ctk.CTkLabel):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            text_color=Colors.ACCENT,
            cursor="hand2",
            **kwargs,
        )
        if command is not None:
            self.bind("<Button-1>", lambda _event: command())
