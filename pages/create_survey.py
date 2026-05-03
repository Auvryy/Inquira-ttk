import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from app.theme_colors import Colors
from components.primary_entry import PrimaryEntry
from components.primary_button import PrimaryButton
from components.tag_chip import TagChip
from models.question_type import QuestionType
from models.survey import SurveyQuestion, SurveySection
from models.survey_creation import SurveyCreation


class CreateSurveyPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app
        self.available_tags = [
            "Academic",
            "Health",
            "Technology",
            "Entertainment",
            "Lifestyle",
            "Business",
            "Research",
            "Marketing",
        ]
        self.available_audiences = [
            "Students",
            "Business Students",
            "General Public",
            "Professionals",
            "Educators",
            "Healthcare Workers",
            "IT Professionals",
            "Researchers",
            "Parents",
            "Senior Citizens",
        ]

        self.step_index = 0
        self.draft = app.state.draft or SurveyCreation()
        if not self.draft.sections:
            self.draft.sections.append(SurveySection(id="section-1", title="Section 1", order=1))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 6))
        self.header.columnconfigure(0, weight=1)

        self.step_label = ctk.CTkLabel(
            self.header,
            text="Step 1 of 4",
            text_color=Colors.TEXT_MUTED,
            font=app.fonts["small"],
        )
        self.step_label.grid(row=0, column=0, sticky="w")

        self.step_title = ctk.CTkLabel(
            self.header,
            text="Survey Details",
            text_color=Colors.TEXT_DARK,
            font=app.fonts["heading"],
        )
        self.step_title.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.step_container = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.step_container.grid(row=1, column=0, sticky="nsew", padx=24)
        self.step_container.columnconfigure(0, weight=1)

        self.footer = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.footer.grid(row=2, column=0, sticky="ew", padx=24, pady=(8, 18))
        self.footer.columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(
            self.footer,
            text="Back",
            fg_color=Colors.CARD,
            text_color=Colors.CUSTOM_BLUE,
            border_width=2,
            border_color=Colors.CUSTOM_BLUE,
            command=self._previous_step,
            width=120,
        )
        self.back_button.grid(row=0, column=0, sticky="w")

        self.next_button = PrimaryButton(self.footer, text="Next", command=self._next_step, width=140)
        self.next_button.grid(row=0, column=2, sticky="e")

        self.steps = [
            self._build_details_step,
            self._build_audience_step,
            self._build_questions_step,
            self._build_review_step,
        ]
        self._render_step()

    def on_show(self):
        self.draft = self.app.state.draft or self.draft
        self._render_step()

    def _clear_step(self):
        for child in self.step_container.winfo_children():
            child.destroy()

    def _render_step(self):
        self._clear_step()
        self.step_label.configure(text=f"Step {self.step_index + 1} of 4")
        self.back_button.configure(state="normal" if self.step_index > 0 else "disabled")
        self.next_button.configure(text="Publish" if self.step_index == 3 else "Next")
        self.steps[self.step_index]()

    def _build_details_step(self):
        self.step_title.configure(text="Survey Details")

        frame = ctk.CTkFrame(
            self.step_container,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        self.title_entry = PrimaryEntry(frame, placeholder="Survey Title")
        self.title_entry.insert(0, self.draft.title)
        self.title_entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.caption_entry = PrimaryEntry(frame, placeholder="Caption")
        self.caption_entry.insert(0, self.draft.caption)
        self.caption_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.description_box = ctk.CTkTextbox(
            frame,
            height=120,
            fg_color=Colors.SURFACE,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        if self.draft.description:
            self.description_box.insert("1.0", self.draft.description)
        self.description_box.grid(row=2, column=0, sticky="ew", pady=(0, 14))

        time_frame = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        time_frame.grid(row=3, column=0, sticky="w", pady=(0, 12))
        ctk.CTkLabel(
            time_frame,
            text="Approximate time:",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        ).pack(side="left", padx=(0, 10))
        self.time_menu = ctk.CTkOptionMenu(
            time_frame,
            values=["3", "10", "20", "40", "60"],
        )
        self.time_menu.set(str(self.draft.time_to_complete))
        self.time_menu.pack(side="left")

        tags_frame = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        tags_frame.grid(row=4, column=0, sticky="w")
        ctk.CTkLabel(
            tags_frame,
            text="Tags (max 3):",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        ).grid(row=0, column=0, sticky="w")

        self.tag_chips = []
        chip_container = ctk.CTkFrame(tags_frame, fg_color=Colors.CARD)
        chip_container.grid(row=1, column=0, sticky="w", pady=(6, 0))

        for idx, tag in enumerate(self.available_tags):
            selected = tag in self.draft.tags
            chip = TagChip(chip_container, text=tag, selected=selected, command=self._on_tag_change)
            chip.grid(row=idx // 4, column=idx % 4, padx=4, pady=4)
            self.tag_chips.append(chip)

    def _build_audience_step(self):
        self.step_title.configure(text="Target Audience")

        frame = ctk.CTkFrame(
            self.step_container,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="Select up to 5 audiences:",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.audience_chips = []
        chip_container = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        chip_container.grid(row=1, column=0, sticky="w")

        for idx, audience in enumerate(self.available_audiences):
            selected = audience in self.draft.target_audience
            chip = TagChip(chip_container, text=audience, selected=selected, command=self._on_audience_change)
            chip.grid(row=idx // 2, column=idx % 2, padx=6, pady=6)
            self.audience_chips.append(chip)

        custom_frame = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        custom_frame.grid(row=2, column=0, sticky="w", pady=(12, 0))

        self.custom_audience_entry = PrimaryEntry(custom_frame, placeholder="Add custom audience")
        self.custom_audience_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            custom_frame,
            text="Add",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._add_custom_audience,
            width=80,
        ).pack(side="left")

    def _build_questions_step(self):
        self.step_title.configure(text="Questions")

        frame = ctk.CTkFrame(
            self.step_container,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame,
            text="Add Question",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._open_question_dialog,
            width=140,
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        self.questions_container = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        self.questions_container.grid(row=1, column=0, sticky="nsew")
        self.questions_container.columnconfigure(0, weight=1)
        self._render_questions()

    def _render_questions(self):
        for child in self.questions_container.winfo_children():
            child.destroy()

        if not self.draft.questions:
            ctk.CTkLabel(
                self.questions_container,
                text="No questions yet. Add your first question.",
                text_color=Colors.SECONDARY_TEXT,
                font=self.app.fonts["small"],
            ).grid(row=0, column=0, pady=20)
            return

        for idx, question in enumerate(self.draft.questions):
            card = ctk.CTkFrame(
                self.questions_container,
                fg_color=Colors.CARD,
                corner_radius=12,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
            )
            card.columnconfigure(0, weight=1)
            card.grid(row=idx, column=0, sticky="ew", pady=6)

            ctk.CTkLabel(
                card,
                text=f"{idx + 1}. {question.text}",
                text_color=Colors.PRIMARY_TEXT,
                font=self.app.fonts["small_bold"],
                wraplength=620,
                justify="left",
            ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))

            ctk.CTkLabel(
                card,
                text=f"Type: {question.type.display_name()}",
                text_color=Colors.SECONDARY_TEXT,
                font=self.app.fonts["small"],
            ).grid(row=1, column=0, sticky="w", padx=12)

            ctk.CTkButton(
                card,
                text="Remove",
                fg_color=Colors.PINK,
                hover_color=Colors.ORANGE,
                text_color=Colors.CARD,
                command=lambda i=idx: self._remove_question(i),
                width=90,
            ).grid(row=0, column=1, rowspan=2, padx=12, pady=10)

    def _build_review_step(self):
        self.step_title.configure(text="Review & Publish")

        frame = ctk.CTkFrame(
            self.step_container,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        summary = [
            f"Title: {self.draft.title}",
            f"Caption: {self.draft.caption}",
            f"Description: {self.draft.description}",
            f"Time: {self.draft.time_to_complete} min",
            f"Tags: {', '.join(self.draft.tags)}",
            f"Audience: {', '.join(self.draft.target_audience)}",
            f"Questions: {len(self.draft.questions)}",
        ]

        ctk.CTkLabel(
            frame,
            text="\n".join(summary),
            text_color=Colors.PRIMARY_TEXT,
            font=self.app.fonts["body"],
            justify="left",
        ).grid(row=0, column=0, sticky="w")

    def _next_step(self):
        if not self._capture_step():
            return
        if self.step_index == 3:
            self._publish()
            return
        self.step_index += 1
        self._render_step()

    def _previous_step(self):
        if self.step_index == 0:
            return
        if not self._capture_step():
            return
        self.step_index -= 1
        self._render_step()

    def _capture_step(self):
        if self.step_index == 0:
            self.draft.title = self.title_entry.get().strip()
            self.draft.caption = self.caption_entry.get().strip()
            self.draft.description = self.description_box.get("1.0", "end").strip()
            self.draft.time_to_complete = int(self.time_menu.get())
            self.draft.tags = [chip.cget("text") for chip in self.tag_chips if chip.selected]
            if not self.draft.title:
                messagebox.showwarning("Validation", "Title is required.")
                return False
        if self.step_index == 1:
            self.draft.target_audience = [chip.cget("text") for chip in self.audience_chips if chip.selected]
            if not self.draft.target_audience:
                messagebox.showwarning("Validation", "Select at least one audience.")
                return False
        if self.step_index == 2:
            if not self.draft.questions:
                messagebox.showwarning("Validation", "Add at least one question.")
                return False
        self.app.state.draft = self.draft
        self.app.state.save()
        return True

    def _publish(self):
        if not self.draft.questions:
            messagebox.showwarning("Validation", "Add at least one question.")
            return
        self.app.state.create_survey(self.draft)
        messagebox.showinfo("Published", "Survey created successfully.")
        self.draft = SurveyCreation()
        self.step_index = 0
        self.app.state.draft = None
        self.app.state.save()
        self._render_step()

    def _on_tag_change(self, _selected):
        selected_tags = [chip.cget("text") for chip in self.tag_chips if chip.selected]
        if len(selected_tags) > 3:
            messagebox.showwarning("Limit", "You can select up to 3 tags.")
            for chip in self.tag_chips:
                if chip.selected and chip.cget("text") == selected_tags[-1]:
                    chip.set_selected(False)
            return

    def _on_audience_change(self, _selected):
        selected = [chip for chip in self.audience_chips if chip.selected]
        if len(selected) > 5:
            messagebox.showwarning("Limit", "You can select up to 5 audiences.")
            for chip in reversed(self.audience_chips):
                if chip.selected:
                    chip.set_selected(False)
                    break

    def _add_custom_audience(self):
        text = self.custom_audience_entry.get().strip()
        if not text:
            return
        if text not in self.available_audiences:
            self.available_audiences.append(text)
        if text not in self.draft.target_audience:
            self.draft.target_audience.append(text)
        self.custom_audience_entry.delete(0, "end")
        self._render_step()

    def _open_question_dialog(self):
        QuestionDialog(self, self._add_question)

    def _add_question(self, question_text, question_type, options, required):
        section_id = self.draft.sections[0].id if self.draft.sections else "section-1"
        new_question = SurveyQuestion(
            id=f"q-{len(self.draft.questions) + 1}",
            text=question_text,
            type=question_type,
            required=required,
            options=options,
            order=len(self.draft.questions),
            section_id=section_id,
        )
        self.draft.questions.append(new_question)
        self._render_questions()

    def _remove_question(self, index):
        if index < 0 or index >= len(self.draft.questions):
            return
        self.draft.questions.pop(index)
        self._render_questions()


class QuestionDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save
        self.title("Add Question")
        self.geometry("520x540")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="New Question",
            text_color=Colors.PRIMARY_TEXT,
            font=("Poppins", 18, "bold"),
        ).pack(pady=(16, 8))

        self.question_entry = PrimaryEntry(self, placeholder="Question text")
        self.question_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.type_menu = ctk.CTkOptionMenu(
            self,
            values=[q.display_name() for q in QuestionType],
        )
        self.type_menu.pack(padx=24, pady=(0, 12))

        self.required_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self,
            text="Required",
            variable=self.required_var,
            fg_color=Colors.ACCENT,
            text_color=Colors.SECONDARY_TEXT,
        ).pack(anchor="w", padx=24, pady=(0, 12))

        ctk.CTkLabel(
            self,
            text="Options (one per line for choice-based questions)",
            text_color=Colors.SECONDARY_TEXT,
            font=("Poppins", 11),
        ).pack(anchor="w", padx=24)

        self.options_box = ctk.CTkTextbox(self, height=120, fg_color=Colors.INPUT)
        self.options_box.pack(fill="x", padx=24, pady=(4, 12))

        ctk.CTkButton(
            self,
            text="Add",
            fg_color=Colors.PRIMARY,
            hover_color=Colors.SHADED_PRIMARY,
            text_color=Colors.BACKGROUND,
            command=self._save,
        ).pack(fill="x", padx=24, pady=(0, 18))

    def _save(self):
        text = self.question_entry.get().strip()
        if not text:
            messagebox.showwarning("Validation", "Question text is required.")
            return
        type_label = self.type_menu.get()
        question_type = next((q for q in QuestionType if q.display_name() == type_label), QuestionType.SHORT_TEXT)
        options_text = self.options_box.get("1.0", "end").strip()
        options = [line.strip() for line in options_text.splitlines() if line.strip()]
        if question_type in (QuestionType.RADIO, QuestionType.CHECKBOX, QuestionType.DROPDOWN) and len(options) < 2:
            messagebox.showwarning("Validation", "Add at least two options for this question type.")
            return
        self.on_save(text, question_type, options, self.required_var.get())
        self.destroy()
