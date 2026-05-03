import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from app.theme_colors import Colors
from app.scroll_utils import bind_scroll_wheel
from models.question_type import QuestionType


class TakeSurveyWindow(ctk.CTkToplevel):
    def __init__(self, parent, app, survey):
        super().__init__(parent)
        self.app = app
        self.survey = survey
        self.answer_vars = {}

        self.title("Take Survey")
        self.geometry("800x720")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text=survey.title,
            text_color=Colors.PRIMARY_TEXT,
            font=app.fonts["heading"],
        ).pack(pady=(18, 4))

        ctk.CTkLabel(
            self,
            text=survey.description or survey.caption,
            text_color=Colors.SECONDARY_TEXT,
            font=app.fonts["small"],
            wraplength=700,
            justify="center",
        ).pack(pady=(0, 12))

        scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.BACKGROUND)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        scroll.columnconfigure(0, weight=1)
        bind_scroll_wheel(scroll)

        if not survey.questions:
            ctk.CTkLabel(
                scroll,
                text="No questions available for this survey.",
                text_color=Colors.SECONDARY_TEXT,
                font=app.fonts["body"],
            ).grid(row=0, column=0, pady=20)
        else:
            for idx, question in enumerate(survey.questions):
                frame = self._build_question(scroll, question, idx + 1)
                frame.grid(row=idx, column=0, sticky="ew", pady=10)

        ctk.CTkButton(
            self,
            text="Submit",
            fg_color=Colors.PRIMARY,
            hover_color=Colors.SHADED_PRIMARY,
            text_color=Colors.BACKGROUND,
            command=self._submit,
        ).pack(pady=(6, 18))

    def _build_question(self, parent, question, number):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        frame.columnconfigure(0, weight=1)

        label_text = f"{number}. {question.text}"
        if question.required:
            label_text += " *"
        ctk.CTkLabel(
            frame,
            text=label_text,
            text_color=Colors.PRIMARY_TEXT,
            font=self.app.fonts["body_bold"],
            wraplength=680,
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 8))

        question_type = question.type
        if isinstance(question_type, str):
            question_type = QuestionType(question_type)

        if question_type in (QuestionType.SHORT_TEXT, QuestionType.EMAIL, QuestionType.NUMBER, QuestionType.DATE):
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            ctk.CTkEntry(
                frame,
                textvariable=var,
                fg_color=Colors.INPUT,
                border_color=Colors.PRIMARY,
                border_width=1,
            ).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        elif question_type == QuestionType.LONG_TEXT:
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            textbox = ctk.CTkTextbox(frame, height=100, fg_color=Colors.INPUT)
            textbox.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
            textbox.bind(
                "<KeyRelease>",
                lambda _e, t=textbox, v=var: v.set(t.get("1.0", "end").strip()),
            )
        elif question_type == QuestionType.RADIO:
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            options = question.options or []
            for i, option in enumerate(options):
                ctk.CTkRadioButton(
                    frame,
                    text=option,
                    value=option,
                    variable=var,
                    text_color=Colors.PRIMARY_TEXT,
                    fg_color=Colors.ACCENT,
                ).grid(row=1 + i, column=0, sticky="w", padx=16)
        elif question_type == QuestionType.CHECKBOX:
            vars_list = []
            options = question.options or []
            for i, option in enumerate(options):
                var = tk.BooleanVar(value=False)
                vars_list.append((option, var))
                ctk.CTkCheckBox(
                    frame,
                    text=option,
                    variable=var,
                    text_color=Colors.PRIMARY_TEXT,
                    fg_color=Colors.ACCENT,
                ).grid(row=1 + i, column=0, sticky="w", padx=16)
            self.answer_vars[question.id] = vars_list
        elif question_type == QuestionType.DROPDOWN:
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            options = question.options or ["Select"]
            ctk.CTkOptionMenu(
                frame,
                values=options,
                variable=var,
            ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))
        elif question_type == QuestionType.RATING:
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            options = [str(i) for i in range(1, (question.max_rating or 5) + 1)]
            ctk.CTkOptionMenu(
                frame,
                values=options,
                variable=var,
            ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))
        else:
            var = tk.StringVar(value="")
            self.answer_vars[question.id] = var
            ctk.CTkEntry(
                frame,
                textvariable=var,
                fg_color=Colors.INPUT,
                border_color=Colors.PRIMARY,
                border_width=1,
            ).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

        return frame

    def _submit(self):
        missing = []
        for question in self.survey.questions:
            if not question.required:
                continue
            value = self.answer_vars.get(question.id)
            if isinstance(value, tk.StringVar):
                if not value.get().strip():
                    missing.append(question.text)
            elif isinstance(value, list):
                if not any(v.get() for _opt, v in value):
                    missing.append(question.text)

        if missing:
            messagebox.showwarning("Incomplete", "Please answer required questions.")
            return

        self.app.state.submit_response(self.survey.id)
        self.destroy()
