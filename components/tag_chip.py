import customtkinter as ctk

from app.theme_colors import Colors


class TagChip(ctk.CTkButton):
    def __init__(self, parent, text, selected=False, command=None, **kwargs):
        self._selected = selected
        self._command = command
        super().__init__(
            parent,
            text=text,
            command=self._toggle,
            fg_color=Colors.PRIMARY if selected else Colors.BACKGROUND,
            text_color=Colors.BACKGROUND if selected else Colors.PRIMARY,
            border_color=Colors.PRIMARY,
            border_width=2,
            corner_radius=8,
            height=30,
            **kwargs,
        )

    def _toggle(self):
        self._selected = not self._selected
        self.configure(
            fg_color=Colors.PRIMARY if self._selected else Colors.BACKGROUND,
            text_color=Colors.BACKGROUND if self._selected else Colors.PRIMARY,
        )
        if self._command:
            self._command(self._selected)

    @property
    def selected(self):
        return self._selected

    def set_selected(self, selected):
        self._selected = selected
        self.configure(
            fg_color=Colors.PRIMARY if self._selected else Colors.BACKGROUND,
            text_color=Colors.BACKGROUND if self._selected else Colors.PRIMARY,
        )
