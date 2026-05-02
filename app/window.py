import customtkinter as ctk

from app.styles import build_fonts, setup_theme
from app.theme_colors import Colors
from app.state import AppState
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.shell import ShellPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        setup_theme()

        self.title("Inquira")
        self.geometry("1200x760")
        self.minsize(1100, 700)
        self.configure(fg_color=Colors.BACKGROUND)

        self.fonts = build_fonts(self)
        self.state = AppState()
        self.state.load()

        self.container = ctk.CTkFrame(self, fg_color=Colors.BACKGROUND)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self._create_pages()

        start_page = "ShellPage" if self.state.is_authenticated else "LoginPage"
        self.show_page(start_page)

    def _create_pages(self):
        self.pages = {
            "LoginPage": LoginPage(self.container, self),
            "RegisterPage": RegisterPage(self.container, self),
            "ShellPage": ShellPage(self.container, self),
        }

        for frame in self.pages.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, name, **kwargs):
        page = self.pages.get(name)
        if page is None:
            return
        page.tkraise()
        if hasattr(page, "on_show"):
            page.on_show(**kwargs)

    def login(self, username, password):
        if self.state.login(username, password):
            self.show_page("ShellPage")
            return True
        return False

    def register(self, username, password):
        if self.state.register(username, password):
            self.show_page("ShellPage")
            return True
        return False

    def logout(self):
        self.state.logout()
        self.show_page("LoginPage")
