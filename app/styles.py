import ttkbootstrap as ttk
from .theme_colors import Colors


def setup_styles():
    style = ttk.Style()

    style.configure(
        "Primary-Button",
        font=("Segoe UI", 12),
        foreground="white",
        background=Colors.PRIMARY,
    )

    style.configure(
        "Primary.TEntry",
        relief="flat",
        bordercolor=Colors.PRIMARY,
        borderwidth=2,
        fieldbackground="white",
        foreground="#000000",
        font=("Segoe UI", 11)
    )

    style.configure(
        "Container.TFrame",
        background=Colors.SURFACE
    )

    style.configure(
        "Card.TFrame",
        background=Colors.BACKGROUND,
        relief="flat"
    )

    style.configure(
        "Card.TLabel",
        background=Colors.BACKGROUND
    )
