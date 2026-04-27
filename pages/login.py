import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from components.primary_button import PrimaryButton


class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=30)

        ttk.Label(self, text="Login", font=("Segoe UI", 24)).pack(pady=20)

        ttk.Entry(self).pack(pady=8, fill=X)
        ttk.Entry(self, show="*").pack(pady=8, fill=X)

        PrimaryButton(self, text="Login  na").pack()

        ttk.Button(
            self,
            text="Go to Register",
            bootstyle=SECONDARY,
            command=lambda: app.show_page("RegisterPage"),
        ).pack()
