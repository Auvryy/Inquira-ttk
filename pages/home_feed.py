import customtkinter as ctk
import tkinter as tk

from app.theme_colors import Colors
from components.primary_entry import PrimaryEntry
from components.survey_card import SurveyCard
from pages.take_survey import TakeSurveyWindow


class HomeFeedPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.BACKGROUND)
        self.app = app
        self.search_var = tk.StringVar(value="")
        self.filter_var = tk.StringVar(value="All")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        search_frame = ctk.CTkFrame(self, fg_color=Colors.BACKGROUND)
        search_frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 8))
        search_frame.columnconfigure(0, weight=1)

        self.search_entry = PrimaryEntry(search_frame, placeholder="Search surveys")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", lambda _e: self.refresh())

        self.filter_menu = ctk.CTkOptionMenu(
            search_frame,
            values=["All"],
            variable=self.filter_var,
            command=lambda _v: self.refresh(),
        )
        self.filter_menu.grid(row=0, column=1)

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color=Colors.SECONDARY_TEXT,
            font=app.fonts["small"],
        )
        self.status_label.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 6))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.BACKGROUND)
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.scroll.columnconfigure(0, weight=1)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_visible_surveys()
        tags = sorted({tag for survey in surveys for tag in survey.tags})
        self.filter_menu.configure(values=["All"] + tags)

        search_text = self.search_entry.get().strip().lower()
        active_filter = self.filter_var.get()

        filtered = []
        for survey in surveys:
            if active_filter != "All" and active_filter not in survey.tags:
                continue
            if search_text and search_text not in survey.title.lower() and search_text not in survey.caption.lower():
                continue
            filtered.append(survey)

        self.status_label.configure(text=f"Showing {len(filtered)} surveys")

        if not filtered:
            ctk.CTkLabel(
                self.scroll,
                text="No surveys match your search yet.",
                text_color=Colors.SECONDARY_TEXT,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, pady=40)
            return

        for idx, survey in enumerate(filtered):
            card = SurveyCard(
                self.scroll,
                survey,
                on_like=self._toggle_like,
                on_take=self._open_survey,
            )
            card.grid(row=idx, column=0, sticky="ew", pady=8)

    def _toggle_like(self, survey):
        self.app.state.toggle_like(survey.id)
        self.refresh()

    def _open_survey(self, survey):
        TakeSurveyWindow(self, self.app, survey)
