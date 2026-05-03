import customtkinter as ctk
from tkinter import messagebox

from app.theme_colors import Colors
from components.primary_entry import PrimaryEntry
from components.primary_button import PrimaryButton


class EditProfileWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user = app.state.current_user

        self.title("Edit Profile")
        self.geometry("420x420")
        self.configure(fg_color=Colors.SURFACE)

        ctk.CTkLabel(
            self,
            text="Profile Details",
            text_color=Colors.PRIMARY_TEXT,
            font=app.fonts["heading"],
        ).pack(pady=(18, 12))

        self.email_entry = PrimaryEntry(self, placeholder="Email")
        self.email_entry.pack(fill="x", padx=24, pady=(0, 12))
        self.school_entry = PrimaryEntry(self, placeholder="School")
        self.school_entry.pack(fill="x", padx=24, pady=(0, 12))
        self.program_entry = PrimaryEntry(self, placeholder="Program")
        self.program_entry.pack(fill="x", padx=24, pady=(0, 12))

        if self.user:
            if self.user.email:
                self.email_entry.insert(0, self.user.email)
            if self.user.school:
                self.school_entry.insert(0, self.user.school)
            if self.user.program:
                self.program_entry.insert(0, self.user.program)

        PrimaryButton(self, text="Save", command=self._save).pack(pady=20, padx=24, fill="x")

    def _save(self):
        if not self.user:
            return
        self.user.email = self.email_entry.get().strip() or None
        self.user.school = self.school_entry.get().strip() or None
        self.user.program = self.program_entry.get().strip() or None
        self.app.state.save()
        messagebox.showinfo("Saved", "Profile updated.")
        self.destroy()
