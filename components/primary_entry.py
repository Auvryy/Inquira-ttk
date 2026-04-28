import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class PrimaryEntry(ttk.Entry):
    """Reusable styled entry with thick black border."""
    def __init__(self, parent, placeholder="", **kwargs):
        # We extract is_password to manage the show="*" logic dynamically
        self.is_password = kwargs.pop("is_password", False)
        
        # Use custom style "Styled.TEntry" and pass through kwargs
        super().__init__(
            parent,
            style="Primary.TEntry",
            **kwargs
        )

        # Optional placeholder behavior
        if placeholder:
            self.placeholder = placeholder
            self.insert(0, placeholder)
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if super().get() == getattr(self, "placeholder", ""):
            self.delete(0, "end")
            if getattr(self, "is_password", False):
                self.configure(show="*")

    def _on_focus_out(self, event):
        if super().get() == "":
            if getattr(self, "is_password", False):
                self.configure(show="")
            self.insert(0, getattr(self, "placeholder", ""))
            
    def set_password_mode(self, is_pwd):
        """Allows dynamically toggling the password mode (e.g. via a Checkbutton)"""
        self.is_password = is_pwd
        if super().get() != getattr(self, "placeholder", ""):
            self.configure(show="*" if is_pwd else "")

    def get(self):
        value = super().get()
        return value if value != getattr(self, "placeholder", "") else ""
