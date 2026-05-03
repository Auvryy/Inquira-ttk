import customtkinter as ctk
import tkinter as tk

from app.theme_colors import Colors
from pages.archived_surveys import ArchivedSurveysPage
from pages.create_survey import CreateSurveyPage
from pages.home_feed import HomeFeedPage
from pages.liked_surveys import LikedSurveysPage
from pages.my_surveys import MySurveysPage
from pages.profile import ProfilePage
from pages.settings import SettingsPage


class ShellPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app
        self.active_section = None
        self.sidebar_visible = True
        self.search_var = tk.StringVar(value="")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            fg_color=Colors.SIDEBAR_BG,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.content_wrapper = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.content_wrapper.grid(row=0, column=1, sticky="nsew")
        self.content_wrapper.rowconfigure(1, weight=1)
        self.content_wrapper.columnconfigure(0, weight=1)

        self._build_sidebar()
        self._build_topbar()
        self._build_sections()

    def _build_sidebar(self):
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color=Colors.SIDEBAR_BG)
        logo_frame.pack(fill="x", padx=18, pady=(20, 10))

        ctk.CTkLabel(
            logo_frame,
            text="Inquira",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["title_md"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Research connect",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).pack(anchor="w", pady=(4, 0))

        self.nav_buttons = {}
        nav_container = ctk.CTkFrame(self.sidebar, fg_color=Colors.SIDEBAR_BG)
        nav_container.pack(fill="x", padx=10, pady=(8, 0))

        self._add_nav_button(nav_container, "Home", "home")
        self._add_nav_button(nav_container, "Create Survey", "create")
        self._add_nav_button(nav_container, "My Surveys", "my_surveys")
        self._add_nav_button(nav_container, "Profile", "profile")

        ctk.CTkLabel(
            nav_container,
            text="Posts",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).pack(anchor="w", padx=6, pady=(16, 6))

        self._add_nav_button(nav_container, "Archived", "archived", is_sub=True)
        self._add_nav_button(nav_container, "Liked", "liked", is_sub=True)

        spacer = ctk.CTkFrame(self.sidebar, fg_color=Colors.SIDEBAR_BG)
        spacer.pack(fill="both", expand=True)

        self.profile_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=Colors.CARD,
            corner_radius=14,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.profile_card.pack(fill="x", padx=16, pady=(0, 16))
        self.profile_card.columnconfigure(1, weight=1)

        self.profile_avatar = ctk.CTkLabel(
            self.profile_card,
            text="",
            width=44,
            height=44,
            fg_color=Colors.CUSTOM_BLUE,
            text_color=Colors.CARD,
            corner_radius=22,
            font=self.app.fonts["body_bold"],
        )
        self.profile_avatar.grid(row=0, column=0, rowspan=2, padx=12, pady=12)

        self.profile_name = ctk.CTkLabel(
            self.profile_card,
            text="",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["body_bold"],
        )
        self.profile_name.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=(14, 2))

        self.profile_school = ctk.CTkLabel(
            self.profile_card,
            text="",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        )
        self.profile_school.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(0, 12))

        actions = ctk.CTkFrame(self.profile_card, fg_color=Colors.CARD)
        actions.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        actions.columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Settings",
            fg_color=Colors.SURFACE,
            hover_color=Colors.SIDEBAR_HOVER,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
            command=lambda: self.show_section("settings"),
            height=30,
        ).grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkButton(
            actions,
            text="Log Out",
            fg_color=Colors.WARNING,
            hover_color=Colors.ORANGE,
            text_color=Colors.CARD,
            command=self.app.logout,
            height=30,
        ).grid(row=1, column=0, sticky="ew")

    def _add_nav_button(self, parent, label, key, is_sub=False):
        btn = ctk.CTkButton(
            parent,
            text=label,
            fg_color=Colors.SIDEBAR_BG,
            hover_color=Colors.SIDEBAR_HOVER,
            text_color=Colors.TEXT_DARK,
            anchor="w",
            corner_radius=10,
            height=36 if not is_sub else 32,
            command=lambda k=key: self.show_section(k),
            font=self.app.fonts["body"] if not is_sub else self.app.fonts["small"],
        )
        btn.pack(fill="x", padx=(4 if not is_sub else 16), pady=2)
        self.nav_buttons[key] = btn

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(
            self.content_wrapper,
            fg_color=Colors.NAV_BG,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.columnconfigure(1, weight=1)

        left = ctk.CTkFrame(self.topbar, fg_color=Colors.NAV_BG)
        left.grid(row=0, column=0, sticky="w", padx=16, pady=12)

        ctk.CTkButton(
            left,
            text="Menu",
            fg_color=Colors.CARD,
            hover_color=Colors.SURFACE,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
            height=32,
            width=70,
            command=self._toggle_sidebar,
        ).pack(side="left")

        self.page_title = ctk.CTkLabel(
            self.topbar,
            text="Home",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["heading"],
        )
        self.page_title.grid(row=0, column=1, sticky="w", padx=16)

        search_frame = ctk.CTkFrame(self.topbar, fg_color=Colors.NAV_BG)
        search_frame.grid(row=0, column=2, sticky="e", padx=16, pady=12)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search surveys...",
            fg_color=Colors.CARD,
            text_color=Colors.TEXT_DARK,
            border_color=Colors.BORDER_LIGHT,
            border_width=1,
            corner_radius=10,
            height=34,
            width=280,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda _e: self._on_search_change())

        self.clear_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            fg_color=Colors.SURFACE,
            hover_color=Colors.SIDEBAR_HOVER,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
            height=34,
            width=70,
            command=self._clear_search,
            state="disabled",
        )
        self.clear_button.pack(side="left", padx=(8, 0))

    def _toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()
        self.sidebar_visible = not self.sidebar_visible

    def _clear_search(self):
        self.search_var.set("")
        self._on_search_change()

    def _on_search_change(self):
        query = self.search_var.get().strip()
        state = "normal" if query else "disabled"
        self.clear_button.configure(state=state)
        home = self.sections.get("home")
        if home and hasattr(home, "set_search_query"):
            home.set_search_query(query)

    def _build_sections(self):
        self.sections = {
            "home": HomeFeedPage(self.content_wrapper, self.app),
            "profile": ProfilePage(self.content_wrapper, self.app),
            "create": CreateSurveyPage(self.content_wrapper, self.app),
            "my_surveys": MySurveysPage(self.content_wrapper, self.app),
            "archived": ArchivedSurveysPage(self.content_wrapper, self.app),
            "liked": LikedSurveysPage(self.content_wrapper, self.app),
            "settings": SettingsPage(self.content_wrapper, self.app),
        }

        for frame in self.sections.values():
            frame.grid(row=1, column=0, sticky="nsew")

    def _update_nav_styles(self):
        for key, btn in self.nav_buttons.items():
            if key == self.active_section:
                btn.configure(
                    fg_color=Colors.SIDEBAR_ACTIVE,
                    hover_color=Colors.BLUE,
                    text_color=Colors.CARD,
                )
            else:
                btn.configure(
                    fg_color=Colors.SIDEBAR_BG,
                    hover_color=Colors.SIDEBAR_HOVER,
                    text_color=Colors.TEXT_DARK,
                )

    def _update_search_state(self):
        is_home = self.active_section == "home"
        self.search_entry.configure(state="normal" if is_home else "disabled")
        if is_home:
            self.clear_button.configure(
                state="normal" if self.search_var.get().strip() else "disabled"
            )
        else:
            self.clear_button.configure(state="disabled")

    def on_show(self, **_kwargs):
        user = self.app.state.current_user
        username = user.username if user else ""
        initials = username[:2].upper() if username else "U"
        school = user.school if user and user.school else "Unknown school"

        self.profile_avatar.configure(text=initials)
        self.profile_name.configure(text=username)
        self.profile_school.configure(text=school)

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
            "archived": "Archived",
            "liked": "Liked",
            "settings": "Settings",
        }
        self.page_title.configure(text=title_map.get(key, "Inquira"))
        self._update_nav_styles()
        self._update_search_state()
