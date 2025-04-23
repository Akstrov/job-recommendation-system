import pytest
import numpy as np
from app.candidate_recommender import CandidateRecommender
from app.vectorizer import JobVectorizer
from app.models import User, Job

@pytest.fixture
def vectorizer():
    vectorizer = JobVectorizer()
    vectorizer.load_vectorizer('d:/studies/AI/job_recommendation_system/models/job_vectorizer.pkl')
    return vectorizer

@pytest.fixture
def recommender(vectorizer):
    return CandidateRecommender(vectorizer)

@pytest.fixture
def test_job():
    return Job(
        id=1,
        title="Senior Python Developer",
        description="Looking for an experienced Python developer with ML expertise",
        required_skills=["python", "machine learning", "django"],
        required_experience=5.0,
        required_education="master",
        location="New York",
        remote_ok=True
    )

@pytest.fixture
def test_candidates():
    return [
        User(
            id=1,
            skills=["python", "machine learning", "django"],
            experience=6.0,
            education=["master, Computer Science"],
            location="New York",
            remote_ok=True
        ),
        User(
            id=2,
            skills=["python", "django"],
            experience=3.0,
            education=["bachelor, Computer Science"],
            location="Remote",
            remote_ok=True
        ),
        User(
            id=3,
            skills=["python", "machine learning", "django", "fastapi"],
            experience=5.0,
            education=["master, Data Science"],
            location="Boston",
            remote_ok=True
        ),
        User(
            id=4,
            skills=["java", "spring"],
            experience=7.0,
            education=["master, Computer Science"],
            location="New York",
            remote_ok=False
        )
    ]

def test_get_recommendations(recommender, test_job, test_candidates):
    recommendations = recommender.get_recommendations(test_job, test_candidates)
    assert len(recommendations) > 0
    # First candidate should be the best match (id=1)
    assert recommendations[0][0].id == 1
    # Java developer (id=4) should not be in recommendations
    assert all(rec[0].id != 4 for rec in recommendations)

def test_apply_hard_requirements(recommender, test_job, test_candidates):
    mask = recommender._apply_hard_requirements(test_job, test_candidates)
    assert isinstance(mask, np.ndarray)
    assert mask.dtype == bool
    # Candidate 2 should be filtered out (insufficient experience and education)
    assert not mask[1]
    # Candidate 4 should be filtered out (missing required skills)
    assert not mask[3]

def test_calculate_skills_match(recommender, test_job, test_candidates):
    scores = recommender._calculate_skills_match(test_job, test_candidates)
    assert isinstance(scores, np.ndarray)
    assert len(scores) == len(test_candidates)
    # Candidate 1 should have perfect skills match
    assert scores[0] == 1.0
    # Candidate 4 should have no skills match
    assert scores[3] == 0.0

def test_empty_candidates(recommender, test_job):
    recommendations = recommender.get_recommendations(test_job, [])
    assert len(recommendations) == 0

def test_no_matching_candidates(recommender, test_job):
    # Create candidates that don't meet requirements
    unqualified_candidates = [
        User(
            id=1,
            skills=["java"],
            experience=1.0,
            education=["bachelor"],
            location="New York",
            remote_ok=True
        )
    ]
    recommendations = recommender.get_recommendations(test_job, unqualified_candidates)
    assert len(recommendations) == 0

def test_recommendations_order(recommender, test_job, test_candidates):
    recommendations = recommender.get_recommendations(test_job, test_candidates)
    scores = [score for _, score, _ in recommendations]
    # Verify scores are in descending order
    assert all(scores[i] >= scores[i+1] for i in range(len(scores)-1))