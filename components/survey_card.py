import customtkinter as ctk
from datetime import datetime

from app.theme_colors import Colors
from components.primary_button import PrimaryButton


class SurveyCard(ctk.CTkFrame):
    def __init__(self, parent, survey, on_like=None, on_take=None):
        super().__init__(
            parent,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self.survey = survey
        self.on_like = on_like
        self.on_take = on_take

        self.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=Colors.CARD)
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))
        header.columnconfigure(1, weight=1)

        avatar = ctk.CTkLabel(
            header,
            text=self._initials(),
            width=44,
            height=44,
            fg_color=Colors.CUSTOM_BLUE,
            text_color=Colors.CARD,
            corner_radius=22,
            font=("Poppins", 12, "bold"),
        )
        avatar.grid(row=0, column=0, rowspan=2, padx=(0, 12))

        ctk.CTkLabel(
            header,
            text=self.survey.creator,
            text_color=Colors.TEXT_DARK,
            font=("Poppins", 13, "bold"),
        ).grid(row=0, column=1, sticky="w")

        created_label = ctk.CTkLabel(
            header,
            text=self._format_date(self.survey.created_at),
            text_color=Colors.TEXT_MUTED,
            font=("Poppins", 11),
        )
        created_label.grid(row=1, column=1, sticky="w")

        status_text, status_color = self._status_info()
        ctk.CTkLabel(
            header,
            text=status_text,
            text_color=Colors.CARD,
            fg_color=status_color,
            corner_radius=8,
            font=("Poppins", 10, "bold"),
            padx=8,
            pady=4,
        ).grid(row=0, column=2, rowspan=2, sticky="e")

        ctk.CTkLabel(
            self,
            text=survey.title,
            text_color=Colors.TEXT_DARK,
            font=("Poppins", 15, "bold"),
            wraplength=680,
            justify="left",
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(4, 4))

        if survey.caption:
            ctk.CTkLabel(
                self,
                text=survey.caption,
                text_color=Colors.TEXT_MUTED,
                font=("Poppins", 12),
                wraplength=680,
                justify="left",
            ).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        tags_frame = ctk.CTkFrame(self, fg_color=Colors.CARD)
        tags_frame.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 10))

        tags = survey.tags if survey.tags else ["General"]
        for idx, tag in enumerate(tags):
            badge = ctk.CTkLabel(
                tags_frame,
                text=f"#{tag}",
                text_color=Colors.TAG_TEXT,
                fg_color=Colors.TAG_BG,
                corner_radius=12,
                font=("Poppins", 10, "bold"),
                padx=8,
                pady=3,
            )
            badge.grid(row=0, column=idx, padx=(0, 6))

        info_row = ctk.CTkFrame(self, fg_color=Colors.CARD)
        info_row.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))
        info_row.columnconfigure(2, weight=1)

        ctk.CTkLabel(
            info_row,
            text=f"{survey.time_to_complete} min",
            text_color=Colors.TEXT_MUTED,
            font=("Poppins", 11, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 14))

        audience = ", ".join(survey.target_audience) if survey.target_audience else "General"
        ctk.CTkLabel(
            info_row,
            text=audience,
            text_color=Colors.TEXT_MUTED,
            font=("Poppins", 11),
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            info_row,
            text=f"{survey.responses} responses",
            text_color=Colors.TEXT_MUTED,
            font=("Poppins", 11),
        ).grid(row=0, column=2, sticky="e")

        actions = ctk.CTkFrame(self, fg_color=Colors.CARD)
        actions.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 14))
        actions.columnconfigure(1, weight=1)

        like_label = f"Like ({survey.num_likes})"
        ctk.CTkButton(
            actions,
            text=like_label,
            fg_color=Colors.SURFACE,
            hover_color=Colors.SIDEBAR_HOVER,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
            command=self._toggle_like,
            height=30,
            width=120,
        ).grid(row=0, column=0, sticky="w")

        PrimaryButton(
            actions,
            text="Take Survey",
            command=self._take_survey,
            width=140,
            height=30,
        ).grid(row=0, column=2, sticky="e")

    def _initials(self):
        name = self.survey.creator or "U"
        return name[:2].upper()

    def _format_date(self, value):
        try:
            return datetime.fromisoformat(value).strftime("%b %d, %Y")
        except Exception:
            return value

    def _status_info(self):
        if not self.survey.approved:
            return "Pending", Colors.TEXT_MUTED
        if self.survey.status:
            return "Open", Colors.SUCCESS
        return "Closed", Colors.ERROR

    def _toggle_like(self):
        if self.on_like:
            self.on_like(self.survey)

    def _take_survey(self):
        if self.on_take:
            self.on_take(self.survey)
