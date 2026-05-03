import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from app.theme_colors import Colors
from components.primary_button import PrimaryButton
from components.primary_entry import PrimaryEntry
from components.secondary_button import SecondaryButton
from components.link_label import LinkLabel


class RegisterPage(ctk.CTkFrame):
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

        ctk.CTkLabel(
            card_frame,
            text="Create Account",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["title_md"],
        ).pack(pady=(22, 6), padx=30)

        ctk.CTkLabel(
            card_frame,
            text="Set up your Inquira profile to get started.",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        ).pack(pady=(0, 18))

        requirements = ctk.CTkLabel(
            card_frame,
            text=(
                "Requirements:\n"
                "- Username must be unique\n"
                "- Password must be at least 8 characters\n"
                "- Include one number and one symbol"
            ),
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
            justify="left",
        )
        requirements.pack(anchor="w", padx=28, pady=(0, 16))

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
        self.username_entry = PrimaryEntry(card_frame, placeholder="Choose a username")
        self.username_entry.pack(fill="x", padx=28, pady=(6, 12))

        ctk.CTkLabel(
            card_frame,
            text="Password",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["small_bold"],
        ).pack(anchor="w", padx=28)
        self.password_entry = PrimaryEntry(card_frame, placeholder="Create a password", is_password=True)
        self.password_entry.pack(fill="x", padx=28, pady=(6, 12))

        ctk.CTkLabel(
            card_frame,
            text="Confirm Password",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["small_bold"],
        ).pack(anchor="w", padx=28)
        self.confirm_entry = PrimaryEntry(card_frame, placeholder="Re-enter your password", is_password=True)
        self.confirm_entry.pack(fill="x", padx=28, pady=(6, 10))

        options_frame = ctk.CTkFrame(card_frame, fg_color=Colors.CARD)
        options_frame.pack(fill="x", padx=28, pady=(0, 12))

        self.accept_terms = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="I agree to the terms and privacy policy",
            variable=self.accept_terms,
            text_color=Colors.TEXT_MUTED,
            fg_color=Colors.CUSTOM_BLUE,
        ).pack(anchor="w")

        self.show_password = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Show passwords",
            variable=self.show_password,
            text_color=Colors.TEXT_MUTED,
            fg_color=Colors.CUSTOM_BLUE,
            command=self._toggle_password,
        ).pack(anchor="w", pady=(8, 0))

        PrimaryButton(card_frame, text="Create Account", command=self._on_register).pack(
            fill="x", padx=28, pady=(0, 10)
        )

        SecondaryButton(card_frame, text="Continue with Google", command=self._google_stub).pack(
            fill="x", padx=28, pady=(0, 12)
        )

        footer = ctk.CTkFrame(card_frame, fg_color=Colors.CARD)
        footer.pack(pady=(2, 8))

        ctk.CTkLabel(
            footer,
            text="Have an account?",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        ).pack(side="left")
        LinkLabel(
            footer,
            text="Login",
            command=lambda: self.app.show_page("LoginPage"),
            font=app.fonts["small_bold"],
        ).pack(side="left", padx=(6, 0))

        LinkLabel(
            card_frame,
            text="Terms and Conditions and Privacy Policy",
            command=self._show_terms,
            font=app.fonts["small"],
        ).pack(pady=(6, 18))

    def _toggle_password(self):
        show_pwd = self.show_password.get()
        self.password_entry.set_password_mode(not show_pwd)
        self.confirm_entry.set_password_mode(not show_pwd)

    def _google_stub(self):
        self.error_label.configure(text="Google sign-in is disabled in desktop mode.")

    def _show_terms(self):
        messagebox.showinfo("Terms", "Terms and privacy policy are not available yet.")

    def _validate(self, username, password, confirm):
        if len(username) < 4 or len(username) > 36:
            return "Username must be 4-36 characters."
        if len(password) < 8:
            return "Password must be at least 8 characters."
        if not any(char.isdigit() for char in password):
            return "Password must include a number."
        if not any(char in "!@#$%^&*()_+-=[]{};:'\",.<>/?" for char in password):
            return "Password must include a symbol."
        if password != confirm:
            return "Passwords do not match."
        if not self.accept_terms.get():
            return "Please accept the terms to continue."
        return ""

    def _on_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        error = self._validate(username, password, confirm)
        if error:
            self.error_label.configure(text=error)
            return

        if not self.app.register(username, password):
            self.error_label.configure(text="Username already exists.")
        else:
            self.error_label.configure(text="")
