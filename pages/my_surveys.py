import customtkinter as ctk
from datetime import datetime

from app.theme_colors import Colors
from app.scroll_utils import bind_scroll_wheel
from pages.edit_survey import EditSurveyWindow
from pages.survey_responses import SurveyResponsesWindow


class MySurveysPage(ctk.CTkFrame):
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
            text="Your Surveys",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.SURFACE)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.scroll.columnconfigure(0, weight=1)
        bind_scroll_wheel(self.scroll)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_user_surveys()
        if not surveys:
            ctk.CTkLabel(
                self.scroll,
                text="You have not created any surveys yet.",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, pady=40)
            return

        for idx, survey in enumerate(surveys):
            card = self._build_card(self.scroll, survey)
            card.grid(row=idx, column=0, sticky="ew", pady=8)

    def _build_card(self, parent, survey):
        frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        frame.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text=survey.title,
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["body_bold"],
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        created = self._format_date(survey.created_at)
        ctk.CTkLabel(
            frame,
            text=f"Created: {created}  |  Responses: {survey.responses}",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).grid(row=1, column=0, sticky="w", padx=16)

        status_text = "Open" if survey.status else "Closed"
        status_color = Colors.SUCCESS if survey.status else Colors.ERROR
        ctk.CTkLabel(
            frame,
            text=f"Status: {status_text}",
            text_color=status_color,
            font=self.app.fonts["small_bold"],
        ).grid(row=2, column=0, sticky="w", padx=16, pady=(4, 8))

        action_row = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        action_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))

        ctk.CTkButton(
            action_row,
            text="Edit",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=lambda s=survey: self._edit_survey(s),
            width=90,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            action_row,
            text="Analytics",
            fg_color=Colors.CARD,
            text_color=Colors.CUSTOM_BLUE,
            border_width=2,
            border_color=Colors.CUSTOM_BLUE,
            command=lambda s=survey: self._open_analytics(s),
            width=110,
        ).pack(side="left")

        ctk.CTkButton(
            action_row,
            text="Archive",
            fg_color=Colors.ORANGE,
            hover_color=Colors.PINK,
            text_color=Colors.BACKGROUND,
            command=lambda s=survey: self._archive_survey(s),
            width=110,
        ).pack(side="right")

        return frame

    def _format_date(self, value):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed.strftime("%b %d, %Y")
        except Exception:
            return value

    def _edit_survey(self, survey):
        EditSurveyWindow(self, self.app, survey, on_saved=self.refresh)

    def _open_analytics(self, survey):
        SurveyResponsesWindow(self, self.app, survey)

    def _archive_survey(self, survey):
        self.app.state.archive_survey(survey.id)
        self.refresh()
