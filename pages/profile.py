import customtkinter as ctk

from app.theme_colors import Colors
from pages.edit_profile import EditProfileWindow


class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app

        self.columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(
            self,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 12))
        self.header.columnconfigure(1, weight=1)

        self.avatar = ctk.CTkLabel(
            self.header,
            text="",
            width=70,
            height=70,
            fg_color=Colors.CUSTOM_BLUE,
            text_color=Colors.CARD,
            corner_radius=35,
            font=app.fonts["title_md"],
        )
        self.avatar.grid(row=0, column=0, rowspan=2, padx=18, pady=18)

        self.name_label = ctk.CTkLabel(
            self.header,
            text="",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["heading"],
        )
        self.name_label.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=(20, 4))

        self.role_label = ctk.CTkLabel(
            self.header,
            text="",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        )
        self.role_label.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(0, 18))

        self.details = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.details.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 12))
        self.details.columnconfigure(0, weight=1)

        self.info_label = ctk.CTkLabel(
            self.details,
            text="",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["body"],
            justify="left",
        )
        self.info_label.grid(row=0, column=0, sticky="w", pady=(0, 12))

        actions = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        actions.grid(row=2, column=0, sticky="w", padx=24)

        ctk.CTkButton(
            actions,
            text="Edit Profile",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._open_edit_profile,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            actions,
            text="Liked Surveys",
            fg_color=Colors.CARD,
            text_color=Colors.CUSTOM_BLUE,
            border_width=2,
            border_color=Colors.CUSTOM_BLUE,
            command=self._open_liked_surveys,
        ).pack(side="left")

    def on_show(self):
        user = self.app.state.current_user
        if not user:
            return
        initials = user.username[:2].upper() if user.username else "U"
        self.avatar.configure(text=initials)
        self.name_label.configure(text=user.username)
        self.role_label.configure(text=user.role.capitalize())

        info_lines = [
            f"Email: {user.email or 'Not set'}",
            f"School: {user.school or 'Not set'}",
            f"Program: {user.program or 'Not set'}",
        ]
        self.info_label.configure(text="\n".join(info_lines))

    def _open_edit_profile(self):
        EditProfileWindow(self, self.app)

    def _open_liked_surveys(self):
        self.app.show_shell_section("liked")
