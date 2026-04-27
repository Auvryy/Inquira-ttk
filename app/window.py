import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pages.login import LoginPage
from pages.register import RegisterPage


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Survey App")
        self.geometry("900x600")
        self.minsize(900, 600)

        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=YES)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.pages = {
            "LoginPage": LoginPage(container, self),
            "RegisterPage": RegisterPage(container, self),
        }

        for frame in self.pages.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("LoginPage")

    def show_page(self, name):
        self.pages[name].tkraise()
