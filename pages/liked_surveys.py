import customtkinter as ctk

from app.theme_colors import Colors
from app.scroll_utils import bind_scroll_wheel
from components.survey_card import SurveyCard
from pages.take_survey import TakeSurveyWindow


class LikedSurveysPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 8))
        header.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Liked Surveys",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Surveys you have liked are saved here.",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.SURFACE)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.scroll.columnconfigure(0, weight=1)
        bind_scroll_wheel(self.scroll)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_liked_surveys()
        if not surveys:
            ctk.CTkLabel(
                self.scroll,
                text="You have not liked any surveys yet.",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, pady=40)
            return

        for idx, survey in enumerate(surveys):
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


class LikedSurveysWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.title("Liked Surveys")
        self.geometry("860x640")
        self.configure(fg_color=Colors.SURFACE)

        page = LikedSurveysPage(self, app)
        page.pack(fill="both", expand=True)
