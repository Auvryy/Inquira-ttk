import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from app.theme_colors import Colors
from components.primary_entry import PrimaryEntry


class EditSurveyWindow(ctk.CTkToplevel):
    def __init__(self, parent, app, survey, on_saved=None):
        super().__init__(parent)
        self.app = app
        self.survey = survey
        self.on_saved = on_saved

        self.title("Edit Survey")
        self.geometry("520x520")
        self.configure(fg_color=Colors.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Edit Survey",
            text_color=Colors.PRIMARY_TEXT,
            font=app.fonts["heading"],
        ).pack(pady=(16, 10))

        self.title_entry = PrimaryEntry(self, placeholder="Title")
        self.title_entry.insert(0, survey.title)
        self.title_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.caption_entry = PrimaryEntry(self, placeholder="Caption")
        self.caption_entry.insert(0, survey.caption)
        self.caption_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.description_box = ctk.CTkTextbox(self, height=120, fg_color=Colors.INPUT)
        self.description_box.insert("1.0", survey.description)
        self.description_box.pack(fill="x", padx=24, pady=(0, 12))

        self.status_var = tk.BooleanVar(value=survey.status)
        ctk.CTkCheckBox(
            self,
            text="Survey is open",
            variable=self.status_var,
            fg_color=Colors.ACCENT,
            text_color=Colors.SECONDARY_TEXT,
        ).pack(anchor="w", padx=24, pady=(0, 18))

        ctk.CTkButton(
            self,
            text="Save",
            fg_color=Colors.PRIMARY,
            hover_color=Colors.SHADED_PRIMARY,
            text_color=Colors.BACKGROUND,
            command=self._save,
        ).pack(fill="x", padx=24, pady=(0, 18))

    def _save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required.")
            return
        caption = self.caption_entry.get().strip()
        description = self.description_box.get("1.0", "end").strip()
        status = self.status_var.get()

        self.app.state.update_survey(
            self.survey.id,
            title=title,
            caption=caption,
            description=description,
            status=status,
        )
        if self.on_saved:
            self.on_saved()
        messagebox.showinfo("Saved", "Survey updated.")
        self.destroy()
