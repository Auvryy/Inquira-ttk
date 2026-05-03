import os
import tkinter as tk
from PIL import Image
import customtkinter as ctk

from app.theme_colors import Colors
from components.primary_button import PrimaryButton
from components.secondary_button import SecondaryButton


class LandingPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="white")
        self.app = app
        self.images = []
        self.section_positions = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_header()
        self._build_scroll()
        self._build_sections()
        self.after(200, self._cache_section_positions)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="white")
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(18, 10))
        header.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="Inquira",
            text_color=Colors.CUSTOM_BLUE,
            font=self.app.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")

        nav = ctk.CTkFrame(header, fg_color="white")
        nav.grid(row=0, column=1, sticky="e")

        self._nav_button(nav, "Home", lambda: self._scroll_to("home")).pack(side="left", padx=6)
        self._nav_button(nav, "About", lambda: self._scroll_to("about")).pack(side="left", padx=6)
        self._nav_button(nav, "Features", lambda: self._scroll_to("features")).pack(side="left", padx=6)

        SecondaryButton(
            nav,
            text="Login",
            command=lambda: self.app.show_page("LoginPage"),
            width=110,
        ).pack(side="left", padx=(18, 6))
        PrimaryButton(
            nav,
            text="Sign Up",
            command=lambda: self.app.show_page("RegisterPage"),
            width=120,
        ).pack(side="left")

    def _build_scroll(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=0)
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.columnconfigure(0, weight=1)

    def _build_sections(self):
        self.sections = {}

        hero = ctk.CTkFrame(self.scroll, fg_color="white")
        hero.grid(row=0, column=0, sticky="ew", padx=60, pady=(10, 40))
        hero.columnconfigure(0, weight=1)
        self.sections["home"] = hero

        hero_title_font = ctk.CTkFont(family=self.app.fonts["title"][0], size=48, weight="bold")
        hero_sub_font = ctk.CTkFont(family=self.app.fonts["title"][0], size=36, weight="bold")

        ctk.CTkLabel(
            hero,
            text="TURNING CURIOSITY",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_title_font,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            hero,
            text="INTO MEANINGFUL",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_title_font,
            anchor="w",
        ).grid(row=1, column=0, sticky="w")

        hero_line = ctk.CTkFrame(hero, fg_color="white")
        hero_line.grid(row=2, column=0, sticky="w")

        ctk.CTkLabel(
            hero_line,
            text="RESEARCH.",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_title_font,
        ).pack(side="left")
        badge = ctk.CTkFrame(hero_line, fg_color=Colors.SECONDARY_BG, corner_radius=28)
        badge.pack(side="left", padx=18)
        ctk.CTkLabel(
            badge,
            text="Inquira",
            text_color=Colors.CUSTOM_BLUE,
            font=hero_sub_font,
        ).pack(padx=18, pady=8)

        ctk.CTkLabel(
            hero,
            text=(
                "Create and share surveys, or discover insights by answering others. "
                "Built for students, researchers, and innovators."
            ),
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["body"],
            wraplength=720,
            justify="left",
        ).grid(row=3, column=0, sticky="w", pady=(12, 0))

        about = ctk.CTkFrame(self.scroll, fg_color="white")
        about.grid(row=1, column=0, sticky="ew", padx=60, pady=(0, 40))
        about.columnconfigure(0, weight=1)
        about.columnconfigure(1, weight=1)
        self.sections["about"] = about

        left = ctk.CTkFrame(about, fg_color="white")
        left.grid(row=0, column=0, sticky="nw")
        ctk.CTkLabel(
            left,
            text="SHAPING THE FUTURE OF DISCOVERY",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_sub_font,
            justify="left",
            wraplength=400,
        ).pack(anchor="w")
        PrimaryButton(left, text="Explore", command=lambda: self._scroll_to("gallery")).pack(
            anchor="w", pady=(18, 0)
        )

        right = ctk.CTkFrame(about, fg_color="white")
        right.grid(row=0, column=1, sticky="ne")
        ctk.CTkFrame(right, fg_color=Colors.CUSTOM_BLUE, height=2).pack(fill="x", pady=(6, 16))
        ctk.CTkLabel(
            right,
            text="Who we are",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        ).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(
            right,
            text=(
                "We are a collective of researchers and innovators shaping ideas into impact. "
                "Together, we turn curiosity into discovery."
            ),
            text_color=Colors.PRIMARY_TEXT,
            font=self.app.fonts["body"],
            wraplength=420,
            justify="left",
        ).pack(anchor="w")

        gallery = ctk.CTkFrame(self.scroll, fg_color="white")
        gallery.grid(row=2, column=0, sticky="ew", padx=60, pady=(0, 40))
        gallery.columnconfigure((0, 1, 2), weight=1, uniform="gallery")
        self.sections["gallery"] = gallery

        gallery_items = [
            {
                "type": "image",
                "image": "phone-inquira.jpg",
                "title": "Innovation",
                "desc": "Build solutions that matter",
            },
            {
                "type": "text",
                "text": (
                    "INQUIRA IS A PLATFORM BUILT FOR CURIOUS MINDS. WE MAKE IT EASIER "
                    "FOR STUDENTS, RESEARCHERS, AND INNOVATORS TO CONNECT, SHARE IDEAS, "
                    "AND TURN QUESTIONS INTO DISCOVERIES."
                ),
            },
            {
                "type": "image",
                "image": "phone-laptop.jpg",
                "title": "Discovery",
                "desc": "Turn curiosity into progress",
            },
            {
                "type": "text",
                "text": (
                    "NOT JUST A TOOL, BUT AN ECOSYSTEM FOR GROWTH. CURIOSITY DRIVES "
                    "COLLABORATION, AND COLLABORATION SPARKS INNOVATION."
                ),
            },
            {
                "type": "image",
                "image": "interview.jpg",
                "title": "Collaboration",
                "desc": "Connect minds, share insight",
            },
            {
                "type": "image",
                "image": "mobile-phone.jpg",
                "title": "Growth",
                "desc": "Learn, evolve, and inspire others",
            },
        ]

        for index, item in enumerate(gallery_items):
            row = index // 3
            col = index % 3
            if item["type"] == "text":
                card = ctk.CTkFrame(
                    gallery,
                    fg_color="white",
                    corner_radius=20,
                    border_width=1,
                    border_color=Colors.BORDER,
                )
                card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
                ctk.CTkLabel(
                    card,
                    text=item["text"],
                    text_color=Colors.PRIMARY_TEXT,
                    font=self.app.fonts["small_bold"],
                    wraplength=260,
                    justify="center",
                ).pack(expand=True, padx=18, pady=18)
            else:
                card = ctk.CTkFrame(
                    gallery,
                    fg_color="white",
                    corner_radius=20,
                    border_width=1,
                    border_color=Colors.BORDER,
                )
                card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
                card.grid_propagate(False)
                card.configure(height=340)

                image = self._load_image(item["image"], (300, 340))
                image_label = ctk.CTkLabel(card, text="", image=image)
                image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

                overlay = ctk.CTkFrame(card, fg_color="transparent")
                overlay.place(relx=0.05, rely=0.72)
                ctk.CTkLabel(
                    overlay,
                    text=item["title"],
                    text_color="white",
                    font=self.app.fonts["body_bold"],
                ).pack(anchor="w")
                ctk.CTkLabel(
                    overlay,
                    text=item["desc"],
                    text_color="white",
                    font=self.app.fonts["small"],
                ).pack(anchor="w")

        features = ctk.CTkFrame(self.scroll, fg_color="white")
        features.grid(row=3, column=0, sticky="ew", padx=60, pady=(10, 40))
        features.columnconfigure(0, weight=1)
        self.sections["features"] = features

        ctk.CTkLabel(
            features,
            text="SMART SURVEY SYSTEM",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_sub_font,
        ).grid(row=0, column=0, pady=(0, 8))
        ctk.CTkLabel(
            features,
            text="Everything you need to create, post, and manage academic surveys.",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["body"],
        ).grid(row=1, column=0, pady=(0, 20))

        feature_list = [
            (
                "Create Survey",
                "Design and configure surveys effortlessly with intuitive tools for every question type.",
                "create",
            ),
            (
                "Post Survey",
                "Publish surveys instantly to your desired participants, ready to collect valuable responses.",
                "post",
            ),
            (
                "Mobile Compatible",
                "Optimized for mobile and desktop, ensuring a smooth experience across all devices.",
                "mobile",
            ),
            (
                "Admin Approval",
                "Submitted surveys undergo review to maintain integrity and compliance.",
                "approval",
            ),
        ]

        for idx, (title, desc, icon_kind) in enumerate(feature_list):
            card = ctk.CTkFrame(
                features,
                fg_color="white",
                corner_radius=20,
                border_width=1,
                border_color=Colors.BORDER,
            )
            card.grid(row=2 + idx, column=0, sticky="ew", pady=8)
            card.columnconfigure(1, weight=1)

            icon = FeatureIcon(card, icon_kind, Colors.PRIMARY_TEXT)
            icon.grid(row=0, column=0, padx=18, pady=18)

            text_frame = ctk.CTkFrame(card, fg_color="white")
            text_frame.grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(
                text_frame,
                text=title,
                text_color=Colors.PRIMARY_TEXT,
                font=self.app.fonts["body_bold"],
            ).pack(anchor="w")
            ctk.CTkLabel(
                text_frame,
                text=desc,
                text_color=Colors.SECONDARY_TEXT,
                font=self.app.fonts["small"],
                wraplength=600,
                justify="left",
            ).pack(anchor="w", pady=(4, 0))

        transition = ctk.CTkFrame(self.scroll, fg_color="white")
        transition.grid(row=4, column=0, sticky="ew", padx=60, pady=(10, 40))
        transition.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            transition,
            text="GATHER. ANALYZE. GROW.",
            text_color=Colors.PRIMARY_TEXT,
            font=hero_sub_font,
        ).grid(row=0, column=0, pady=(0, 6))
        ctk.CTkLabel(
            transition,
            text=(
                "Transform data into meaningful insights with Inquira. "
                "Empowering academic excellence through modern survey systems."
            ),
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["body"],
            wraplength=700,
        ).grid(row=1, column=0)

        footer = ctk.CTkFrame(self.scroll, fg_color="white")
        footer.grid(row=5, column=0, sticky="ew", padx=60, pady=(10, 60))
        footer.columnconfigure(0, weight=1)
        self.sections["footer"] = footer

        ctk.CTkLabel(
            footer,
            text="Inquira",
            text_color=Colors.CUSTOM_BLUE,
            font=self.app.fonts["heading"],
        ).grid(row=0, column=0, pady=(0, 6))
        ctk.CTkLabel(
            footer,
            text="Empowering academic research with modern survey tools.",
            text_color=Colors.PRIMARY_TEXT,
            font=self.app.fonts["body"],
        ).grid(row=1, column=0, pady=(0, 12))

        action_row = ctk.CTkFrame(footer, fg_color="white")
        action_row.grid(row=2, column=0, pady=(0, 8))
        SecondaryButton(
            action_row,
            text="Login",
            command=lambda: self.app.show_page("LoginPage"),
            width=120,
        ).pack(side="left", padx=6)
        PrimaryButton(
            action_row,
            text="Sign Up",
            command=lambda: self.app.show_page("RegisterPage"),
            width=120,
        ).pack(side="left", padx=6)

        ctk.CTkLabel(
            footer,
            text="Copyright 2026 Inquira. All rights reserved.",
            text_color=Colors.SECONDARY_TEXT,
            font=self.app.fonts["small"],
        ).grid(row=3, column=0, pady=(8, 0))

    def _nav_button(self, parent, text, command):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color="white",
            hover_color=Colors.SECONDARY_BG,
            text_color=Colors.PRIMARY_TEXT,
            border_width=1,
            border_color=Colors.BORDER,
            corner_radius=20,
            height=34,
        )

    def _load_image(self, filename, size):
        path = os.path.join("assets", "images", filename)
        if not os.path.exists(path):
            return None
        image = ctk.CTkImage(Image.open(path), size=size)
        self.images.append(image)
        return image

    def _cache_section_positions(self):
        try:
            canvas = self.scroll._parent_canvas
        except AttributeError:
            return

        self.scroll.update_idletasks()
        region = canvas.bbox("all")
        if not region:
            return
        region_height = max(1, region[3] - region[1])

        for key, section in self.sections.items():
            self.section_positions[key] = section.winfo_y() / region_height

    def _scroll_to(self, key):
        if key not in self.section_positions:
            self._cache_section_positions()
        position = self.section_positions.get(key)
        if position is None:
            return
        try:
            canvas = self.scroll._parent_canvas
            canvas.yview_moveto(position)
        except AttributeError:
            return


class FeatureIcon(ctk.CTkFrame):
    def __init__(self, parent, kind, color):
        super().__init__(parent, fg_color="white")
        self.canvas = tk.Canvas(self, width=48, height=48, bg="white", highlightthickness=0)
        self.canvas.pack()
        self._draw_icon(kind, color)

    def _draw_icon(self, kind, color):
        if kind == "create":
            self.canvas.create_rectangle(10, 8, 38, 40, outline=color, width=2)
            self.canvas.create_line(16, 16, 32, 16, fill=color, width=2)
            self.canvas.create_line(16, 24, 32, 24, fill=color, width=2)
            self.canvas.create_line(16, 32, 28, 32, fill=color, width=2)
        elif kind == "post":
            self.canvas.create_rectangle(8, 14, 40, 36, outline=color, width=2)
            self.canvas.create_oval(14, 20, 20, 26, outline=color, width=2)
            self.canvas.create_oval(28, 20, 34, 26, outline=color, width=2)
            self.canvas.create_line(22, 23, 26, 23, fill=color, width=2)
        elif kind == "mobile":
            self.canvas.create_rectangle(16, 6, 32, 42, outline=color, width=2)
            self.canvas.create_oval(22, 34, 26, 38, outline=color, width=2)
        elif kind == "approval":
            self.canvas.create_polygon(12, 10, 24, 4, 36, 10, 34, 32, 24, 40, 14, 32, outline=color, width=2, fill="")
            self.canvas.create_line(18, 22, 23, 27, fill=color, width=2)
            self.canvas.create_line(23, 27, 31, 19, fill=color, width=2)
