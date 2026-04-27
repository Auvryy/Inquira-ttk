import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class PrimaryButton(ttk.Button):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent, text=text, command=command, style="Primary-Button", **kwargs
        )
