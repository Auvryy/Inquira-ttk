from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    password: str
    role: str = "user"
    email: Optional[str] = None
    school: Optional[str] = None
    program: Optional[str] = None
    profile_pic: Optional[str] = None

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "email": self.email,
            "school": self.school,
            "program": self.program,
            "profile_pic": self.profile_pic,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "user"),
            email=data.get("email"),
            school=data.get("school"),
            program=data.get("program"),
            profile_pic=data.get("profile_pic"),
        )
