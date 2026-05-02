import customtkinter as ctk
from tkinter import font

from .theme_colors import Colors


def setup_theme():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")


def build_fonts(root):
    families = set(font.families(root))

    def pick_family(preferred):
        for name in preferred:
            if name in families:
                return name
        return "Segoe UI"

    title_family = pick_family(["Giaza", "Poppins", "Segoe UI", "Arial"])
    body_family = pick_family(["Poppins", "Segoe UI", "Arial"])

    return {
        "title": (title_family, 30, "bold"),
        "title_md": (title_family, 22, "bold"),
        "heading": (body_family, 18, "bold"),
        "body": (body_family, 14, "normal"),
        "body_bold": (body_family, 14, "bold"),
        "small": (body_family, 12, "normal"),
        "small_bold": (body_family, 12, "bold"),
    }


def surface_color():
    return Colors.SECONDARY_BG
