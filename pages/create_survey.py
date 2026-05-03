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
        self.step_container.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 12))
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

        content = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        content.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        content.columnconfigure(0, weight=1)

        content = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        content.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        content.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content,
            text="Survey title",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).grid(row=0, column=0, sticky="w")
        self.title_entry = PrimaryEntry(content, placeholder="e.g. Campus Technology Access")
        self.title_entry.insert(0, self.draft.title)
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(6, 12))

        ctk.CTkLabel(
            content,
            text="Caption",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).grid(row=2, column=0, sticky="w")
        self.caption_entry = PrimaryEntry(content, placeholder="Short summary for the feed")
        self.caption_entry.insert(0, self.draft.caption)
        self.caption_entry.grid(row=3, column=0, sticky="ew", pady=(6, 12))

        ctk.CTkLabel(
            content,
            text="Description",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).grid(row=4, column=0, sticky="w")
        self.description_box = ctk.CTkTextbox(
            content,
            height=120,
            fg_color=Colors.SURFACE,
            text_color=Colors.TEXT_DARK,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        if self.draft.description:
            self.description_box.insert("1.0", self.draft.description)
        self.description_box.grid(row=5, column=0, sticky="ew", pady=(6, 16))

        time_frame = ctk.CTkFrame(content, fg_color=Colors.CARD)
        time_frame.grid(row=6, column=0, sticky="w", pady=(0, 12))
        ctk.CTkLabel(
            time_frame,
            text="Approximate time",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).pack(side="left", padx=(0, 10))
        self.time_menu = ctk.CTkOptionMenu(
            time_frame,
            values=["3", "10", "20", "40", "60"],
        )
        self.time_menu.set(str(self.draft.time_to_complete))
        self.time_menu.pack(side="left")

        tags_frame = ctk.CTkFrame(content, fg_color=Colors.CARD)
        tags_frame.grid(row=7, column=0, sticky="w")
        ctk.CTkLabel(
            tags_frame,
            text="Tags (max 3)",
            text_color=Colors.TEXT_MUTED,
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

        content = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        content.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        content.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content,
            text="Select up to 5 audiences",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.audience_chips = []
        chip_container = ctk.CTkFrame(content, fg_color=Colors.CARD)
        chip_container.grid(row=1, column=0, sticky="w")

        for idx, audience in enumerate(self.available_audiences):
            selected = audience in self.draft.target_audience
            chip = TagChip(chip_container, text=audience, selected=selected, command=self._on_audience_change)
            chip.grid(row=idx // 2, column=idx % 2, padx=6, pady=6)
            self.audience_chips.append(chip)

        ctk.CTkLabel(
            content,
            text="Custom audience",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).grid(row=2, column=0, sticky="w", pady=(12, 6))

        custom_frame = ctk.CTkFrame(content, fg_color=Colors.CARD)
        custom_frame.grid(row=3, column=0, sticky="w")

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

        content = ctk.CTkFrame(frame, fg_color=Colors.CARD)
        content.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        content.columnconfigure(0, weight=1)

        header_row = ctk.CTkFrame(content, fg_color=Colors.CARD)
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header_row.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_row,
            text="Survey questions",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["body_bold"],
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header_row,
            text="Add Question",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._open_question_dialog,
            width=140,
            height=32,
        ).grid(row=0, column=1, sticky="e")

        self.questions_container = ctk.CTkFrame(content, fg_color=Colors.CARD)
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
                text_color=Colors.TEXT_MUTED,
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
                text_color=Colors.TEXT_DARK,
                font=self.app.fonts["small_bold"],
                wraplength=620,
                justify="left",
            ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))

            ctk.CTkLabel(
                card,
                text=f"Type: {question.type.display_name()}",
                text_color=Colors.TEXT_MUTED,
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
            content,
            text="\n".join(summary),
            text_color=Colors.TEXT_DARK,
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
        self.app = parent.app
        self.on_save = on_save
        self.options = []
        self.choice_types = {QuestionType.RADIO, QuestionType.CHECKBOX, QuestionType.DROPDOWN}

        self.title("Add Question")
        self.geometry("560x620")
        self.configure(fg_color=Colors.SURFACE)

        card = ctk.CTkFrame(
            self,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="both", expand=True, padx=18, pady=18)
        card.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="New Question",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["heading"],
        ).pack(anchor="w", padx=20, pady=(18, 10))

        ctk.CTkLabel(
            card,
            text="Question text",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).pack(anchor="w", padx=20)
        self.question_entry = PrimaryEntry(card, placeholder="Type your question")
        self.question_entry.pack(fill="x", padx=20, pady=(6, 12))

        ctk.CTkLabel(
            card,
            text="Question type",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).pack(anchor="w", padx=20)
        self.type_menu = ctk.CTkOptionMenu(
            card,
            values=[q.display_name() for q in QuestionType],
            command=self._on_type_change,
        )
        self.type_menu.pack(fill="x", padx=20, pady=(6, 12))

        self.required_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            card,
            text="Required",
            variable=self.required_var,
            fg_color=Colors.CUSTOM_BLUE,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w", padx=20, pady=(0, 12))

        self.options_section = ctk.CTkFrame(card, fg_color=Colors.CARD)
        self.options_section.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.options_section,
            text="Options",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["small_bold"],
        ).grid(row=0, column=0, sticky="w")

        option_row = ctk.CTkFrame(self.options_section, fg_color=Colors.CARD)
        option_row.grid(row=1, column=0, sticky="ew", pady=(6, 8))
        option_row.columnconfigure(0, weight=1)

        self.option_entry = PrimaryEntry(option_row, placeholder="Add option")
        self.option_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.option_entry.bind("<Return>", lambda _e: self._add_option())

        ctk.CTkButton(
            option_row,
            text="Add",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._add_option,
            width=80,
        ).grid(row=0, column=1)

        self.options_list = ctk.CTkFrame(self.options_section, fg_color=Colors.CARD)
        self.options_list.grid(row=2, column=0, sticky="ew")
        self.options_list.columnconfigure(0, weight=1)

        self._toggle_options_section(self._selected_type())
        self._render_options()

        ctk.CTkButton(
            card,
            text="Add",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=self._save,
            height=36,
        ).pack(fill="x", padx=20, pady=(8, 18))

    def _selected_type(self):
        type_label = self.type_menu.get()
        return next(
            (q for q in QuestionType if q.display_name() == type_label),
            QuestionType.SHORT_TEXT,
        )

    def _on_type_change(self, value):
        question_type = next(
            (q for q in QuestionType if q.display_name() == value),
            QuestionType.SHORT_TEXT,
        )
        self._toggle_options_section(question_type)

    def _toggle_options_section(self, question_type):
        if question_type in self.choice_types:
            if not self.options_section.winfo_ismapped():
                self.options_section.pack(fill="x", padx=20, pady=(0, 12))
        else:
            self.options_section.pack_forget()

    def _add_option(self):
        option = self.option_entry.get().strip()
        if not option:
            return
        self.options.append(option)
        self.option_entry.delete(0, "end")
        self._render_options()

    def _remove_option(self, index):
        if index < 0 or index >= len(self.options):
            return
        self.options.pop(index)
        self._render_options()

    def _render_options(self):
        for child in self.options_list.winfo_children():
            child.destroy()

        if not self.options:
            ctk.CTkLabel(
                self.options_list,
                text="No options added yet.",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["small"],
            ).grid(row=0, column=0, sticky="w", pady=(0, 6))
            return

        for idx, option in enumerate(self.options):
            row = ctk.CTkFrame(
                self.options_list,
                fg_color=Colors.SURFACE,
                corner_radius=10,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
            )
            row.grid(row=idx, column=0, sticky="ew", pady=4)
            row.columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row,
                text=option,
                text_color=Colors.TEXT_DARK,
                font=self.app.fonts["small"],
            ).grid(row=0, column=0, sticky="w", padx=10, pady=6)

            ctk.CTkButton(
                row,
                text="Remove",
                fg_color=Colors.SURFACE,
                hover_color=Colors.SIDEBAR_HOVER,
                text_color=Colors.TEXT_DARK,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
                command=lambda i=idx: self._remove_option(i),
                width=90,
                height=26,
            ).grid(row=0, column=1, padx=8, pady=6)

    def _save(self):
        text = self.question_entry.get().strip()
        if not text:
            messagebox.showwarning("Validation", "Question text is required.")
            return
        question_type = self._selected_type()
        options = list(self.options)
        if question_type in self.choice_types and len(options) < 2:
            messagebox.showwarning("Validation", "Add at least two options for this question type.")
            return
        self.on_save(text, question_type, options, self.required_var.get())
        self.destroy()
