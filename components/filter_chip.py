import customtkinter as ctk

from app.theme_colors import Colors


class FilterChip(ctk.CTkButton):
    def __init__(self, parent, text, selected=False, command=None, **kwargs):
        self.value = text
        self._selected = selected
        self._command = command
        super().__init__(
            parent,
            text=text,
            command=self._on_click,
            fg_color=Colors.CUSTOM_BLUE if selected else Colors.CARD,
            text_color=Colors.CARD if selected else Colors.TEXT_DARK,
            hover_color=Colors.BLUE if selected else Colors.SURFACE,
            border_color=Colors.CUSTOM_BLUE if selected else Colors.BORDER_LIGHT,
            border_width=1,
            corner_radius=16,
            height=30,
            **kwargs,
        )

    def _on_click(self):
        if self._command:
            self._command(self)

    def set_selected(self, selected):
        self._selected = selected
        self.configure(
            fg_color=Colors.CUSTOM_BLUE if self._selected else Colors.CARD,
            text_color=Colors.CARD if self._selected else Colors.TEXT_DARK,
            hover_color=Colors.BLUE if self._selected else Colors.SURFACE,
            border_color=Colors.CUSTOM_BLUE if self._selected else Colors.BORDER_LIGHT,
        )

    @property
    def selected(self):
        return self._selected
