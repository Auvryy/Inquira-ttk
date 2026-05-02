import customtkinter as ctk

from app.theme_colors import Colors


class SurveyResponsesWindow(ctk.CTkToplevel):
    def __init__(self, parent, app, survey):
        super().__init__(parent)
        self.app = app
        self.survey = survey

        self.title("Survey Analytics")
        self.geometry("520x420")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Survey Analytics",
            text_color=Colors.PRIMARY_TEXT,
            font=app.fonts["heading"],
        ).pack(pady=(18, 8))

        ctk.CTkLabel(
            self,
            text=survey.title,
            text_color=Colors.SECONDARY_TEXT,
            font=app.fonts["body_bold"],
            wraplength=460,
            justify="center",
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            self,
            text=f"Total responses: {survey.responses}",
            text_color=Colors.PRIMARY,
            font=app.fonts["body"],
        ).pack(pady=(6, 16))

        ctk.CTkLabel(
            self,
            text="Detailed analytics are available once the backend is connected.",
            text_color=Colors.SECONDARY_TEXT,
            font=app.fonts["small"],
            wraplength=420,
            justify="center",
        ).pack(pady=(0, 18))
