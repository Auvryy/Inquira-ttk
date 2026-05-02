import json
from datetime import datetime
from pathlib import Path

from models.question_type import QuestionType
from models.survey import Survey, SurveyQuestion, SurveySection
from models.user import User


class Store:
    def __init__(self):
        self.path = Path(__file__).resolve().parent / "store.json"
        self.data = {
            "users": [],
            "surveys": [],
            "session": {},
            "drafts": {},
            "responses": {},
        }

    def load(self):
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = self._default_data()
        else:
            self.data = self._default_data()
        if not self.data.get("surveys"):
            self._seed_data()

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def _default_data(self):
        return {
            "users": [],
            "surveys": [],
            "session": {},
            "drafts": {},
            "responses": {},
        }

    def _seed_data(self):
        demo_user = User(username="demo", password="demo1234", role="user")
        self.data["users"] = [demo_user.to_dict()]

        section = SurveySection(
            id="section-1",
            title="General",
            description="",
            order=1,
        )

        questions = [
            SurveyQuestion(
                id="q-1",
                text="What motivates you to participate in surveys?",
                type=QuestionType.LONG_TEXT,
                required=True,
                order=0,
                section_id=section.id,
            ),
            SurveyQuestion(
                id="q-2",
                text="How often do you answer online surveys?",
                type=QuestionType.RADIO,
                required=True,
                options=["Daily", "Weekly", "Monthly", "Rarely"],
                order=1,
                section_id=section.id,
            ),
        ]

        surveys = [
            Survey(
                id="survey-1",
                title="Understanding Student Research Habits",
                caption="Help us learn how students discover research topics.",
                description="We want to know how students find and evaluate research ideas.",
                time_to_complete=10,
                tags=["Academic", "Research"],
                target_audience=["Students", "Researchers"],
                creator="demo",
                created_at=datetime.utcnow().isoformat(),
                status=True,
                approved=True,
                archived=False,
                responses=12,
                num_likes=4,
                liked_by=[],
                questions=questions,
                sections=[section],
            ),
            Survey(
                id="survey-2",
                title="Campus Technology Access",
                caption="Share how you access digital tools for schoolwork.",
                description="This survey explores device access and study habits.",
                time_to_complete=5,
                tags=["Technology", "Academic"],
                target_audience=["Students"],
                creator="demo",
                created_at=datetime.utcnow().isoformat(),
                status=True,
                approved=True,
                archived=False,
                responses=7,
                num_likes=2,
                liked_by=[],
                questions=questions,
                sections=[section],
            ),
        ]

        self.data["surveys"] = [s.to_dict() for s in surveys]
