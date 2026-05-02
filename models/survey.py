from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .question_type import QuestionType


@dataclass
class SurveyQuestion:
    id: str
    text: str
    type: QuestionType
    required: bool = False
    options: List[str] = field(default_factory=list)
    min_choice: Optional[int] = None
    max_choice: Optional[int] = None
    max_rating: Optional[int] = None
    image_path: Optional[str] = None
    video_url: Optional[str] = None
    order: int = 0
    section_id: str = "default"

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type.value,
            "required": self.required,
            "options": self.options,
            "min_choice": self.min_choice,
            "max_choice": self.max_choice,
            "max_rating": self.max_rating,
            "image_path": self.image_path,
            "video_url": self.video_url,
            "order": self.order,
            "section_id": self.section_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            text=data.get("text", ""),
            type=QuestionType(data.get("type", QuestionType.SHORT_TEXT.value)),
            required=data.get("required", False),
            options=list(data.get("options", [])),
            min_choice=data.get("min_choice"),
            max_choice=data.get("max_choice"),
            max_rating=data.get("max_rating"),
            image_path=data.get("image_path"),
            video_url=data.get("video_url"),
            order=data.get("order", 0),
            section_id=data.get("section_id", "default"),
        )


@dataclass
class SurveySection:
    id: str
    title: str
    description: str = ""
    order: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            order=data.get("order", 0),
        )


@dataclass
class Survey:
    id: str
    title: str
    caption: str
    description: str
    time_to_complete: int
    tags: List[str]
    target_audience: List[str]
    creator: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: bool = True
    approved: bool = True
    archived: bool = False
    responses: int = 0
    num_likes: int = 0
    liked_by: List[str] = field(default_factory=list)
    questions: List[SurveyQuestion] = field(default_factory=list)
    sections: List[SurveySection] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "caption": self.caption,
            "description": self.description,
            "time_to_complete": self.time_to_complete,
            "tags": self.tags,
            "target_audience": self.target_audience,
            "creator": self.creator,
            "created_at": self.created_at,
            "status": self.status,
            "approved": self.approved,
            "archived": self.archived,
            "responses": self.responses,
            "num_likes": self.num_likes,
            "liked_by": self.liked_by,
            "questions": [q.to_dict() for q in self.questions],
            "sections": [s.to_dict() for s in self.sections],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            caption=data.get("caption", ""),
            description=data.get("description", ""),
            time_to_complete=data.get("time_to_complete", 5),
            tags=list(data.get("tags", [])),
            target_audience=list(data.get("target_audience", [])),
            creator=data.get("creator", ""),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            status=data.get("status", True),
            approved=data.get("approved", True),
            archived=data.get("archived", False),
            responses=data.get("responses", 0),
            num_likes=data.get("num_likes", 0),
            liked_by=list(data.get("liked_by", [])),
            questions=[SurveyQuestion.from_dict(q) for q in data.get("questions", [])],
            sections=[SurveySection.from_dict(s) for s in data.get("sections", [])],
        )
