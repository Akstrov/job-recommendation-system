from dataclasses import dataclass

@dataclass
class MockUser:
    skills: list
    education: list
    experience: float
    location: str
    remote_ok: bool

@dataclass
class MockJob:
    title: str
    description: str
    required_skills: list
    required_education: str
    required_experience: float
    location: str
    remote_ok: bool