import customtkinter as ctk

from app.theme_colors import Colors
from components.survey_card import SurveyCard
from pages.take_survey import TakeSurveyWindow


class LikedSurveysWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.title("Liked Surveys")
        self.geometry("860x640")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Liked Surveys",
            text_color=Colors.PRIMARY_TEXT,
            font=app.fonts["heading"],
        ).pack(pady=(16, 8))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.BACKGROUND)
        self.scroll.pack(fill="both", expand=True, padx=24, pady=12)
        self.scroll.columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_liked_surveys()
        if not surveys:
            ctk.CTkLabel(
                self.scroll,
                text="You have not liked any surveys yet.",
                text_color=Colors.SECONDARY_TEXT,
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
