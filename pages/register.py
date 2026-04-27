import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class RegisterPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=30)

        ttk.Label(self, text="Register", font=("Segoe UI", 24)).pack(pady=20)

        ttk.Entry(self).pack(pady=8, fill=X)
        ttk.Entry(self).pack(pady=8, fill=X)
        ttk.Entry(self, show="*").pack(pady=8, fill=X)

        ttk.Button(self, text="Create Account", bootstyle=SUCCESS).pack(pady=12)

        ttk.Button(
            self,
            text="Back to Login",
            bootstyle=SECONDARY,
            command=lambda: app.show_page("LoginPage"),
        ).pack()
