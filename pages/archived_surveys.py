import customtkinter as ctk

from app.theme_colors import Colors


class ArchivedSurveysPage(ctk.CTkFrame):
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
            text="Archived Surveys",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Restore surveys you have archived.",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.SURFACE)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        self.scroll.columnconfigure(0, weight=1)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_archived_surveys()
        if not surveys:
            ctk.CTkLabel(
                self.scroll,
                text="No archived surveys yet.",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, pady=40)
            return

        for idx, survey in enumerate(surveys):
            frame = ctk.CTkFrame(
                self.scroll,
                fg_color=Colors.CARD,
                corner_radius=16,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
            )
            frame.columnconfigure(0, weight=1)
            frame.grid(row=idx, column=0, sticky="ew", pady=8)

            ctk.CTkLabel(
                frame,
                text=survey.title,
                text_color=Colors.TEXT_DARK,
                font=self.app.fonts["body_bold"],
            ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

            ctk.CTkLabel(
                frame,
                text=f"Responses: {survey.responses}",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["small"],
            ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

            ctk.CTkButton(
                frame,
                text="Unarchive",
                fg_color=Colors.CUSTOM_BLUE,
                hover_color=Colors.BLUE,
                text_color=Colors.CARD,
                command=lambda s=survey: self._unarchive(s),
                width=120,
            ).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

    def _unarchive(self, survey):
        self.app.state.unarchive_survey(survey.id)
        self.refresh()


class ArchivedSurveysWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.title("Archived Surveys")
        self.geometry("760x560")
        self.configure(fg_color=Colors.SURFACE)

        page = ArchivedSurveysPage(self, app)
        page.pack(fill="both", expand=True)
