from dataclasses import dataclass, field
from typing import List, Optional

from .survey import SurveyQuestion, SurveySection


@dataclass
class SurveyCreation:
    title: str = ""
    caption: str = ""
    description: str = ""
    time_to_complete: int = 3
    tags: List[str] = field(default_factory=list)
    target_audience: List[str] = field(default_factory=list)
    questions: List[SurveyQuestion] = field(default_factory=list)
    sections: List[SurveySection] = field(default_factory=list)
    bypass_code: Optional[str] = None

    def to_dict(self):
        return {
            "title": self.title,
            "caption": self.caption,
            "description": self.description,
            "time_to_complete": self.time_to_complete,
            "tags": self.tags,
            "target_audience": self.target_audience,
            "questions": [q.to_dict() for q in self.questions],
            "sections": [s.to_dict() for s in self.sections],
            "bypass_code": self.bypass_code,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title", ""),
            caption=data.get("caption", ""),
            description=data.get("description", ""),
            time_to_complete=data.get("time_to_complete", 3),
            tags=list(data.get("tags", [])),
            target_audience=list(data.get("target_audience", [])),
            questions=[SurveyQuestion.from_dict(q) for q in data.get("questions", [])],
            sections=[SurveySection.from_dict(s) for s in data.get("sections", [])],
            bypass_code=data.get("bypass_code"),
        )
