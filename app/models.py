from sqlalchemy import Column, Integer, String, Boolean, Float, JSON, Text
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base  # Fix this import to use the absolute path

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    skills = Column(SQLiteJSON)  # Store skills as JSON array
    experience = Column(Float)  # Total years of experience
    education = Column(SQLiteJSON)  # Store education as JSON array of "level, institute"
    location = Column(String)  # Store location as "city, country"
    remote_ok = Column(Boolean, default=False)
    tfidf_vector = Column(SQLiteJSON)  # Store vector as JSON array

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(SQLiteJSON)  # Store required skills as JSON array
    required_experience = Column(Float)
    required_education = Column(String)  # Store education as level
    location = Column(String)  # Store location as "city, country"
    remote_ok = Column(Boolean, default=False)
    tfidf_vector = Column(SQLiteJSON)  # Store vector as JSON array