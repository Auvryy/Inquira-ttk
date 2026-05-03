import customtkinter as ctk

from app.theme_colors import Colors
from app.scroll_utils import bind_scroll_wheel
from components.filter_chip import FilterChip
from components.survey_card import SurveyCard
from pages.take_survey import TakeSurveyWindow


class HomeFeedPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=Colors.SURFACE)
        self.app = app
        self.search_query = ""
        self.active_category = "all"
        self.category_chips = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Colors.SURFACE)
        self.scroll.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        self.scroll.columnconfigure(0, weight=1)
        bind_scroll_wheel(self.scroll)

    def on_show(self):
        self.refresh()

    def set_search_query(self, query):
        self.search_query = query.strip()
        self.refresh()

    def refresh(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        surveys = self.app.state.get_visible_surveys()
        categories = self._build_categories(surveys)
        if self.active_category not in categories:
            self.active_category = "all"

        filtered = self._filter_surveys(surveys)

        row = 0
        if self.search_query:
            results_card = ctk.CTkFrame(
                self.scroll,
                fg_color=Colors.CARD,
                corner_radius=14,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
            )
            results_card.grid(row=row, column=0, sticky="ew", pady=(0, 12))
            results_card.columnconfigure(0, weight=1)
            ctk.CTkLabel(
                results_card,
                text=f"Showing results for '{self.search_query}' ({len(filtered)} found)",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["small"],
            ).grid(row=0, column=0, sticky="w", padx=16, pady=12)
            row += 1

        create_card = ctk.CTkFrame(
            self.scroll,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        create_card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        create_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            create_card,
            text="Create a New Survey",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["heading"],
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            create_card,
            text="Start gathering insights from your audience today.",
            text_color=Colors.TEXT_MUTED,
            font=self.app.fonts["small"],
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        ctk.CTkButton(
            create_card,
            text="Create Survey",
            fg_color=Colors.CUSTOM_BLUE,
            hover_color=Colors.BLUE,
            text_color=Colors.CARD,
            command=lambda: self.app.show_shell_section("create"),
            width=140,
            height=32,
        ).grid(row=0, column=1, rowspan=2, padx=16, pady=16, sticky="e")

        row += 1

        filter_card = ctk.CTkFrame(
            self.scroll,
            fg_color=Colors.CARD,
            corner_radius=16,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        filter_card.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        filter_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            filter_card,
            text="Filter by category",
            text_color=Colors.TEXT_DARK,
            font=self.app.fonts["body_bold"],
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        chips_frame = ctk.CTkFrame(filter_card, fg_color=Colors.CARD)
        chips_frame.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        self.category_chips = []
        for idx, category in enumerate(categories):
            chip = FilterChip(
                chips_frame,
                text=self._format_category(category),
                selected=category == self.active_category,
                command=self._on_category_selected,
            )
            chip.category_id = category
            chip.grid(row=idx // 4, column=idx % 4, padx=4, pady=4, sticky="w")
            self.category_chips.append(chip)

        row += 1

        if not filtered:
            empty_card = ctk.CTkFrame(
                self.scroll,
                fg_color=Colors.CARD,
                corner_radius=16,
                border_width=1,
                border_color=Colors.BORDER_LIGHT,
            )
            empty_card.grid(row=row, column=0, sticky="ew", pady=(0, 12))
            ctk.CTkLabel(
                empty_card,
                text="No surveys found. Try adjusting your filters.",
                text_color=Colors.TEXT_MUTED,
                font=self.app.fonts["body"],
            ).grid(row=0, column=0, padx=16, pady=24)
            return

        for idx, survey in enumerate(filtered):
            card = SurveyCard(
                self.scroll,
                survey,
                on_like=self._toggle_like,
                on_take=self._open_survey,
            )
            card.grid(row=row + idx, column=0, sticky="ew", pady=8)

    def _filter_surveys(self, surveys):
        search_text = self.search_query.lower()
        filtered = []
        for survey in surveys:
            tags = [tag.lower() for tag in survey.tags]
            if self.active_category != "all" and self.active_category not in tags:
                continue
            if search_text:
                haystack = " ".join(
                    [
                        survey.title or "",
                        survey.caption or "",
                        survey.description or "",
                        survey.creator or "",
                    ]
                ).lower()
                if search_text not in haystack:
                    continue
            filtered.append(survey)
        return filtered

    def _build_categories(self, surveys):
        base = [
            "all",
            "academic",
            "health",
            "technology",
            "entertainment",
            "lifestyle",
            "business",
            "research",
            "marketing",
        ]
        found = {tag.lower() for survey in surveys for tag in survey.tags}
        categories = []
        for name in base:
            if name not in categories:
                categories.append(name)
        for name in sorted(found):
            if name not in categories:
                categories.append(name)
        return categories

    def _format_category(self, category):
        if category == "all":
            return "All"
        return category.replace("_", " ").title()

    def _on_category_selected(self, chip):
        self.active_category = chip.category_id
        for item in self.category_chips:
            item.set_selected(item.category_id == self.active_category)
        self.refresh()

    def _toggle_like(self, survey):
        self.app.state.toggle_like(survey.id)
        self.refresh()

    def _open_survey(self, survey):
        TakeSurveyWindow(self, self.app, survey)
