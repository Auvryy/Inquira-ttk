from enum import Enum


class QuestionType(str, Enum):
    SHORT_TEXT = "shortText"
    LONG_TEXT = "longText"
    RADIO = "radioButton"
    CHECKBOX = "checkBox"
    RATING = "rating"
    DROPDOWN = "dropdown"
    DATE = "date"
    EMAIL = "email"
    NUMBER = "number"

    def display_name(self):
        display = {
            QuestionType.SHORT_TEXT: "Short Text",
            QuestionType.LONG_TEXT: "Long Text",
            QuestionType.RADIO: "Single Choice",
            QuestionType.CHECKBOX: "Multiple Choice",
            QuestionType.RATING: "Rating",
            QuestionType.DROPDOWN: "Dropdown",
            QuestionType.DATE: "Date",
            QuestionType.EMAIL: "Email",
            QuestionType.NUMBER: "Number",
        }
        return display.get(self, self.value)
