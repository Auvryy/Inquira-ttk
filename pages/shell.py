import customtkinter as ctk

from app.theme_colors import Colors
from pages.home_feed import HomeFeedPage
from pages.create_survey import CreateSurveyPage
from pages.profile import ProfilePage
from pages.my_surveys import MySurveysPage
from pages.settings import SettingsPage


class ShellPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.BACKGROUND)
        self.app = app
        self.active_section = None

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=Colors.PRIMARY)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.content_wrapper = ctk.CTkFrame(self, fg_color=Colors.BACKGROUND)
        self.content_wrapper.grid(row=0, column=1, sticky="nsew")
        self.content_wrapper.rowconfigure(1, weight=1)
        self.content_wrapper.columnconfigure(0, weight=1)

        self._build_sidebar()
        self._build_header()
        self._build_sections()

    def _build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="Inquira",
            text_color=Colors.BACKGROUND,
            font=self.app.fonts["title_md"],
        ).pack(pady=(26, 18))

        self.nav_buttons = {}
        items = [
            ("Home", "home"),
            ("Profile", "profile"),
            ("Create Survey", "create"),
            ("My Surveys", "my_surveys"),
            ("Settings", "settings"),
        ]
        for label, key in items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                fg_color=Colors.PRIMARY,
                hover_color=Colors.SHADED_PRIMARY,
                text_color=Colors.BACKGROUND,
                corner_radius=0,
                height=44,
                command=lambda k=key: self.show_section(k),
            )
            btn.pack(fill="x", padx=0, pady=2)
            self.nav_buttons[key] = btn

        ctk.CTkButton(
            self.sidebar,
            text="Log Out",
            fg_color=Colors.PINK,
            hover_color=Colors.ORANGE,
            text_color=Colors.BACKGROUND,
            corner_radius=0,
            height=44,
            command=self.app.logout,
        ).pack(fill="x", padx=0, pady=(18, 6))

    def _build_header(self):
        self.header = ctk.CTkFrame(self.content_wrapper, fg_color=Colors.SECONDARY_BG)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.columnconfigure(1, weight=1)

        self.page_title = ctk.CTkLabel(
            self.header,
            text="Home",
            text_color=Colors.PRIMARY_TEXT,
            font=self.app.fonts["heading"],
        )
        self.page_title.grid(row=0, column=0, padx=24, pady=18, sticky="w")

        self.user_label = ctk.CTkLabel(
            self.header,
            text="",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        )
        self.user_label.grid(row=0, column=1, padx=24, sticky="e")

    def _build_sections(self):
        self.sections = {
            "home": HomeFeedPage(self.content_wrapper, self.app),
            "profile": ProfilePage(self.content_wrapper, self.app),
            "create": CreateSurveyPage(self.content_wrapper, self.app),
            "my_surveys": MySurveysPage(self.content_wrapper, self.app),
            "settings": SettingsPage(self.content_wrapper, self.app),
        }

        for frame in self.sections.values():
            frame.grid(row=1, column=0, sticky="nsew")

    def on_show(self, **_kwargs):
        username = self.app.state.current_user.username if self.app.state.current_user else ""
        self.user_label.configure(text=username)
        self.show_section("home")

    def show_section(self, key):
        if key not in self.sections:
            return
        self.active_section = key
        for section_key, frame in self.sections.items():
            if section_key == key:
                frame.tkraise()
                if hasattr(frame, "on_show"):
                    frame.on_show()
        title_map = {
            "home": "Home",
            "profile": "Profile",
            "create": "Create Survey",
            "my_surveys": "My Surveys",
            "settings": "Settings",
        }
        self.page_title.configure(text=title_map.get(key, "Inquira"))
