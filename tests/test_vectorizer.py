import pandas as pd
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorizer import JobVectorizer
from dataclasses import dataclass
from app.utils import get_data_path, get_models_path

@dataclass
class MockJob:
    title: str
    description: str
    required_skills: list
    required_education: str
    required_experience: float
    location: str = "Remote"
    remote_ok: bool = True

@dataclass
class MockUser:
    skills: list
    education: list
    experience: float
    location: str = "Remote"
    remote_ok: bool = True

# Remove PROJECT_ROOT constant and update paths
@pytest.fixture
def trained_vectorizer():
    vectorizer = JobVectorizer()
    df = pd.read_csv(get_data_path('linkedin_jobs.csv'))
    
    jobs = [
        MockJob(
            title=row['title'],
            description=row['description'],
            required_skills=['python', 'sql'] if pd.notna(row['skills_desc']) else [],
            required_education='bachelor',
            required_experience=3.0
        )
        for _, row in df.head(1000).iterrows()
    ]
    
    vectorizer.fit(jobs)
    return vectorizer

def test_vectorizer_training(trained_vectorizer):
    assert trained_vectorizer.is_fitted()

def test_vectorizer_save_load(trained_vectorizer, tmp_path):
    save_path = tmp_path / "test_vectorizer.pkl"
    trained_vectorizer.save_vectorizer(str(save_path))
    
    new_vectorizer = JobVectorizer()
    new_vectorizer.load_vectorizer(str(save_path))
    
    assert new_vectorizer.is_fitted()

def test_vectorizer_transform():
    vectorizer = JobVectorizer()
    vectorizer.load_vectorizer(get_models_path('job_vectorizer.pkl'))
    
    test_user = MockUser(
        skills=['python', 'machine learning', 'data analysis'],
        education=['bachelor, Computer Science', 'master, Data Science'],
        experience=5.0
    )
    
    test_job = MockJob(
        title="Data Scientist",
        description="Looking for a Python expert with ML skills",
        required_skills=['python', 'machine learning'],
        required_education='master',
        required_experience=3.0
    )
    
    user_vector = vectorizer.transform_user(test_user)
    job_vector = vectorizer.transform_job(test_job)
    
    assert user_vector is not None
    assert job_vector is not None
    assert user_vector.shape == job_vector.shape