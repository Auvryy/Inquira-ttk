from datetime import datetime
from typing import List, Optional

from data.store import Store
from models.survey import Survey
from models.survey_creation import SurveyCreation
from models.user import User


class AppState:
    def __init__(self):
        self.store = Store()
        self.users: List[User] = []
        self.surveys: List[Survey] = []
        self.current_user: Optional[User] = None
        self.draft: Optional[SurveyCreation] = None

    @property
    def is_authenticated(self):
        return self.current_user is not None

    def load(self):
        self.store.load()
        self.users = [User.from_dict(u) for u in self.store.data.get("users", [])]
        self.surveys = [Survey.from_dict(s) for s in self.store.data.get("surveys", [])]
        session_user = self.store.data.get("session", {}).get("current_user")
        if session_user:
            self.current_user = next((u for u in self.users if u.username == session_user), None)
        self._load_draft()

    def save(self):
        self.store.data["users"] = [u.to_dict() for u in self.users]
        self.store.data["surveys"] = [s.to_dict() for s in self.surveys]
        self._save_draft()
        self.store.save()

    def _save_draft(self):
        if not self.current_user:
            return
        if self.draft is None:
            self.store.data.setdefault("drafts", {}).pop(self.current_user.username, None)
            return
        self.store.data.setdefault("drafts", {})[self.current_user.username] = self.draft.to_dict()

    def _load_draft(self):
        if not self.current_user:
            self.draft = None
            return
        drafts = self.store.data.get("drafts", {})
        if self.current_user.username in drafts:
            self.draft = SurveyCreation.from_dict(drafts[self.current_user.username])
        else:
            self.draft = None

    def login(self, username, password):
        user = next((u for u in self.users if u.username == username), None)
        if not user or user.password != password:
            return False
        self.current_user = user
        self.store.data.setdefault("session", {})["current_user"] = user.username
        self._load_draft()
        self.save()
        return True

    def register(self, username, password):
        if not username or not password:
            return False
        if any(u.username == username for u in self.users):
            return False
        new_user = User(username=username, password=password, role="user")
        self.users.append(new_user)
        self.current_user = new_user
        self.store.data.setdefault("session", {})["current_user"] = new_user.username
        self.save()
        return True

    def logout(self):
        self.current_user = None
        self.store.data["session"] = {}
        self.save()

    def get_visible_surveys(self):
        return [s for s in self.surveys if not s.archived and s.approved]

    def get_user_surveys(self):
        if not self.current_user:
            return []
        return [s for s in self.surveys if s.creator == self.current_user.username and not s.archived]

    def get_archived_surveys(self):
        if not self.current_user:
            return []
        return [s for s in self.surveys if s.creator == self.current_user.username and s.archived]

    def get_liked_surveys(self):
        if not self.current_user:
            return []
        return [s for s in self.surveys if self.current_user.username in s.liked_by]

    def toggle_like(self, survey_id):
        if not self.current_user:
            return
        survey = next((s for s in self.surveys if s.id == survey_id), None)
        if not survey:
            return
        if self.current_user.username in survey.liked_by:
            survey.liked_by.remove(self.current_user.username)
            survey.num_likes = max(0, survey.num_likes - 1)
        else:
            survey.liked_by.append(self.current_user.username)
            survey.num_likes += 1
        self.save()

    def create_survey(self, creation: SurveyCreation):
        if not self.current_user:
            return None
        survey = Survey(
            id=f"survey-{int(datetime.utcnow().timestamp())}",
            title=creation.title,
            caption=creation.caption,
            description=creation.description,
            time_to_complete=creation.time_to_complete,
            tags=list(creation.tags),
            target_audience=list(creation.target_audience),
            creator=self.current_user.username,
            created_at=datetime.utcnow().isoformat(),
            status=True,
            approved=True,
            archived=False,
            responses=0,
            num_likes=0,
            liked_by=[],
            questions=list(creation.questions),
            sections=list(creation.sections),
        )
        self.surveys.insert(0, survey)
        self.draft = None
        self.save()
        return survey

    def update_survey(self, survey_id, title=None, caption=None, description=None, status=None):
        survey = next((s for s in self.surveys if s.id == survey_id), None)
        if not survey:
            return False
        if title is not None:
            survey.title = title
        if caption is not None:
            survey.caption = caption
        if description is not None:
            survey.description = description
        if status is not None:
            survey.status = status
        self.save()
        return True

    def archive_survey(self, survey_id):
        survey = next((s for s in self.surveys if s.id == survey_id), None)
        if not survey:
            return False
        survey.archived = True
        self.save()
        return True

    def unarchive_survey(self, survey_id):
        survey = next((s for s in self.surveys if s.id == survey_id), None)
        if not survey:
            return False
        survey.archived = False
        self.save()
        return True

    def submit_response(self, survey_id):
        survey = next((s for s in self.surveys if s.id == survey_id), None)
        if not survey:
            return False
        survey.responses += 1
        self.save()
        return True
