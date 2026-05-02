import customtkinter as ctk

from app.theme_colors import Colors
from components.primary_button import PrimaryButton
from components.secondary_button import SecondaryButton


class SurveyCard(ctk.CTkFrame):
    def __init__(self, parent, survey, on_like=None, on_take=None):
        super().__init__(parent, fg_color="white", corner_radius=14, border_width=1, border_color=Colors.BORDER)
        self.survey = survey
        self.on_like = on_like
        self.on_take = on_take

        self.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="white")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))
        header.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=survey.title,
            text_color=Colors.PRIMARY_TEXT,
            font=("Poppins", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")

        status_text = "Open" if survey.status else "Closed"
        status_color = Colors.GREEN if survey.status else Colors.ERROR
        ctk.CTkLabel(
            header,
            text=status_text,
            text_color=status_color,
            font=("Poppins", 12, "bold"),
        ).grid(row=0, column=1, sticky="e")

        meta = ctk.CTkLabel(
            self,
            text=f"{survey.creator}  |  {survey.time_to_complete} min",
            text_color=Colors.SECONDARY,
            font=("Poppins", 12),
        )
        meta.grid(row=1, column=0, sticky="w", padx=16)

        if survey.caption:
            ctk.CTkLabel(
                self,
                text=survey.caption,
                text_color=Colors.PRIMARY_TEXT,
                font=("Poppins", 12),
                wraplength=640,
                justify="left",
            ).grid(row=2, column=0, sticky="w", padx=16, pady=(6, 4))

        tags_text = ", ".join(survey.tags) if survey.tags else "No tags"
        audience_text = ", ".join(survey.target_audience) if survey.target_audience else "General"
        ctk.CTkLabel(
            self,
            text=f"Tags: {tags_text}",
            text_color=Colors.SECONDARY_TEXT,
            font=("Poppins", 11),
        ).grid(row=3, column=0, sticky="w", padx=16)
        ctk.CTkLabel(
            self,
            text=f"Audience: {audience_text}",
            text_color=Colors.SECONDARY_TEXT,
            font=("Poppins", 11),
        ).grid(row=4, column=0, sticky="w", padx=16, pady=(0, 6))

        footer = ctk.CTkFrame(self, fg_color="white")
        footer.grid(row=5, column=0, sticky="ew", padx=16, pady=(4, 12))
        footer.columnconfigure(0, weight=1)

        like_text = f"Like ({survey.num_likes})"
        SecondaryButton(footer, text=like_text, command=self._toggle_like, width=120).grid(row=0, column=0, sticky="w")
        PrimaryButton(footer, text="Take Survey", command=self._take_survey, width=140).grid(row=0, column=1, sticky="e")

    def _toggle_like(self):
        if self.on_like:
            self.on_like(self.survey)

    def _take_survey(self):
        if self.on_take:
            self.on_take(self.survey)
