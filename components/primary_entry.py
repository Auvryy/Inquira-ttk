import customtkinter as ctk

from app.theme_colors import Colors


class PrimaryEntry(ctk.CTkEntry):
    def __init__(self, parent, placeholder="", is_password=False, **kwargs):
        self.is_password = is_password
        super().__init__(
            parent,
            placeholder_text=placeholder,
            fg_color=Colors.CARD,
            text_color=Colors.TEXT_DARK,
            border_color=Colors.BORDER_LIGHT,
            border_width=1,
            corner_radius=10,
            show="*" if is_password else "",
            **kwargs,
        )

    def set_password_mode(self, is_pwd):
        self.is_password = is_pwd
        self.configure(show="*" if is_pwd else "")
