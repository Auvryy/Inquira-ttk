import customtkinter as ctk

from app.theme_colors import Colors


class ArchivedSurveysWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.title("Archived Surveys")
        self.geometry("760x560")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Archived Surveys",
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

        surveys = self.app.state.get_archived_surveys()
        if not surveys:
            ctk.CTkLabel(
                self.scroll,
                text="No archived surveys yet.",
                text_color=Colors.SECONDARY_TEXT,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, pady=40)
            return

        for idx, survey in enumerate(surveys):
            frame = ctk.CTkFrame(self.scroll, fg_color="white", corner_radius=12, border_width=1, border_color=Colors.BORDER)
            frame.columnconfigure(0, weight=1)
            frame.grid(row=idx, column=0, sticky="ew", pady=8)

            ctk.CTkLabel(
                frame,
                text=survey.title,
                text_color=Colors.PRIMARY_TEXT,
                font=self.app.fonts["body_bold"],
            ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

            ctk.CTkLabel(
                frame,
                text=f"Responses: {survey.responses}",
                text_color=Colors.SECONDARY,
                font=self.app.fonts["small"],
            ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

            ctk.CTkButton(
                frame,
                text="Unarchive",
                fg_color=Colors.PRIMARY,
                hover_color=Colors.SHADED_PRIMARY,
                text_color=Colors.BACKGROUND,
                command=lambda s=survey: self._unarchive(s),
                width=120,
            ).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

    def _unarchive(self, survey):
        self.app.state.unarchive_survey(survey.id)
        self.refresh()
