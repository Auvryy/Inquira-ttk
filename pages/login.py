import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from app.theme_colors import Colors
from components.primary_button import PrimaryButton
from components.primary_entry import PrimaryEntry
from components.secondary_button import SecondaryButton
from components.link_label import LinkLabel


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        form_container = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        form_container.grid(row=0, column=0, sticky="nsew", padx=32, pady=32)
        form_container.rowconfigure(0, weight=1)
        form_container.columnconfigure(0, weight=1)

        card_frame = ctk.CTkFrame(
            form_container,
            fg_color=Colors.CARD,
            corner_radius=18,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card_frame.grid(row=0, column=0, padx=12, pady=12)

        title = ctk.CTkLabel(
            card_frame,
            text="Inquira",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["title"],
        )
        title.pack(pady=(24, 6), padx=30)

        subtitle = ctk.CTkLabel(
            card_frame,
            text=(
                "Create and share surveys, or steal insights by answering others."
            ),
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
            wraplength=360,
            justify="center",
        )
        subtitle.pack(pady=(0, 18), padx=24)

        self.error_label = ctk.CTkLabel(
            card_frame,
            text="",
            text_color=Colors.ERROR,
            font=app.fonts["small"],
        )
        self.error_label.pack(pady=(0, 10))

        ctk.CTkLabel(
            card_frame,
            text="Username",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["small_bold"],
        ).pack(anchor="w", padx=28)
        self.username_entry = PrimaryEntry(card_frame, placeholder="Enter your username")
        self.username_entry.pack(fill="x", padx=28, pady=(6, 12))

        ctk.CTkLabel(
            card_frame,
            text="Password",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["small_bold"],
        ).pack(anchor="w", padx=28)
        self.password_entry = PrimaryEntry(card_frame, placeholder="Enter your password", is_password=True)
        self.password_entry.pack(fill="x", padx=28, pady=(6, 10))

        options_frame = ctk.CTkFrame(card_frame, fg_color=Colors.CARD)
        options_frame.pack(fill="x", padx=28, pady=(0, 16))

        self.show_password = tk.BooleanVar(value=False)
        show_toggle = ctk.CTkCheckBox(
            options_frame,
            text="Show password",
            variable=self.show_password,
            text_color=Colors.TEXT_MUTED,
            fg_color=Colors.CUSTOM_BLUE,
            command=self._toggle_password,
        )
        show_toggle.pack(side="left")

        LinkLabel(
            options_frame,
            text="Forgot password?",
            command=self._forgot_password,
            font=app.fonts["small"],
        ).pack(side="right")

        PrimaryButton(card_frame, text="Login", command=self._on_login).pack(
            fill="x", padx=28, pady=(0, 12)
        )

        SecondaryButton(card_frame, text="Continue with Google", command=self._google_stub).pack(
            fill="x", padx=28, pady=(0, 12)
        )

        footer = ctk.CTkFrame(card_frame, fg_color=Colors.CARD)
        footer.pack(pady=(4, 10))

        ctk.CTkLabel(
            footer,
            text="Don't have an account?",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        ).pack(side="left")
        LinkLabel(
            footer,
            text="Register",
            command=lambda: self.app.show_page("RegisterPage"),
            font=app.fonts["small_bold"],
        ).pack(side="left", padx=(6, 0))

        LinkLabel(
            card_frame,
            text="Terms and Conditions and Privacy Policy",
            command=self._show_terms,
            font=app.fonts["small"],
        ).pack(pady=(6, 18))

    def _toggle_password(self):
        self.password_entry.set_password_mode(not self.show_password.get())

    def _forgot_password(self):
        self.error_label.configure(text="Password reset is not available in mock mode.")

    def _google_stub(self):
        self.error_label.configure(text="Google sign-in is disabled in desktop mode.")

    def _show_terms(self):
        messagebox.showinfo("Terms", "Terms and privacy policy are not available yet.")

    def _on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Enter your username and password.")
            return

        if not self.app.login(username, password):
            self.error_label.configure(text="Invalid credentials. Try demo/demo1234.")
        else:
            self.error_label.configure(text="")
