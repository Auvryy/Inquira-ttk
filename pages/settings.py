import customtkinter as ctk
from tkinter import messagebox

from app.theme_colors import Colors
from pages.edit_profile import EditProfileWindow


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app

        self.columnconfigure(0, weight=1)

        self.profile_card = ctk.CTkFrame(
            self,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.profile_card.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 12))
        self.profile_card.columnconfigure(1, weight=1)

        self.avatar = ctk.CTkLabel(
            self.profile_card,
            text="",
            width=60,
            height=60,
            fg_color=Colors.CUSTOM_BLUE,
            text_color=Colors.CARD,
            corner_radius=30,
            font=app.fonts["title_md"],
        )
        self.avatar.grid(row=0, column=0, padx=18, pady=18)

        self.user_label = ctk.CTkLabel(
            self.profile_card,
            text="",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["body_bold"],
        )
        self.user_label.grid(row=0, column=1, sticky="w", padx=(0, 12))

        ctk.CTkButton(
            self.profile_card,
            text="Edit",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._edit_profile,
            width=90,
        ).grid(row=0, column=2, padx=18)

        actions = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        actions.grid(row=1, column=0, sticky="ew", padx=24)
        actions.columnconfigure(0, weight=1)

        self._action_button(actions, "Change Password", self._change_password).grid(row=0, column=0, sticky="ew", pady=6)
        self._action_button(actions, "Archived Surveys", self._open_archived).grid(row=1, column=0, sticky="ew", pady=6)
        self._action_button(actions, "Log Out", self.app.logout, danger=True).grid(row=2, column=0, sticky="ew", pady=6)

    def _action_button(self, parent, text, command, danger=False):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=Colors.WARNING if danger else Colors.CARD,
            hover_color=Colors.ORANGE if danger else Colors.SURFACE,
            text_color=Colors.CARD if danger else Colors.TEXT_DARK,
            border_width=0 if danger else 1,
            border_color=Colors.BORDER_LIGHT,
            corner_radius=12,
            height=44,
        )

    def on_show(self):
        user = self.app.state.current_user
        if not user:
            return
        initials = user.username[:2].upper() if user.username else "U"
        self.avatar.configure(text=initials)
        self.user_label.configure(text=user.username)

    def _edit_profile(self):
        EditProfileWindow(self, self.app)

    def _change_password(self):
        messagebox.showinfo("Not available", "Password changes require backend support.")

    def _open_archived(self):
        self.app.show_shell_section("archived")
