import ttkbootstrap as ttk
from .theme_colors import Colors


def setup_styles():
    style = ttk.Style()

    style.configure(
        "Primary-Button",
        font=("Segoe UI", 12),
        foreground="white",
        background=Colors.PRIMARY,
        corner_radous=20,
    )
