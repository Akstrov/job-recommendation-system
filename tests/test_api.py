from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db
from app.models import User, Job

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["vectorizer"] in ["ready", "not ready"]
    assert data["version"] == "1.0.0"

# Update the setup_database fixture to add more test users
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Create test users with various profiles
    test_users = [
        User(
            id=1,
            skills=['python', 'machine learning'],
            experience=3.0,
            education=['bachelor, Computer Science'],
            location='New York',
            remote_ok=True
        ),
        User(
            id=2,
            skills=['python', 'django', 'fastapi'],
            experience=5.0,
            education=['master, Computer Science'],
            location='Boston',
            remote_ok=True
        ),
        User(
            id=3,
            skills=['java', 'spring'],
            experience=4.0,
            education=['bachelor, Software Engineering'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=4,
            skills=['python', 'machine learning', 'tensorflow', 'deep learning'],
            experience=6.0,
            education=['phd, Computer Science'],
            location='New York',
            remote_ok=False
        ),
        User(
            id=5,
            skills=['python', 'django', 'javascript'],
            experience=2.0,
            education=['associate, Web Development'],
            location='Remote',
            remote_ok=True
        )
    ]
    
    # Create test jobs (existing code remains the same)
    test_jobs = [
        Job(
            id=1,
            title='Python Developer',
            description='Looking for a Python expert',
            required_skills=['python', 'django'],
            required_experience=2.0,
            required_education='bachelor',
            location='New York',
            remote_ok=True
        ),
        Job(
            id=2,
            title='Data Scientist',
            description='ML expert needed',
            required_skills=['python', 'machine learning'],
            required_experience=3.0,
            required_education='master',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=3,
            title='Python Engineer',
            description='Python backend developer needed',
            required_skills=['python', 'fastapi'],
            required_experience=2.0,
            required_education='bachelor',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=4,
            title='ML Engineer',
            description='Python and ML expert needed',
            required_skills=['python', 'machine learning', 'tensorflow'],
            required_experience=4.0,
            required_education='master',
            location='New York',
            remote_ok=False
        )
    ]
    
    db.add_all(test_users)
    db.add_all(test_jobs)
    db.commit()
    
    yield
    
    Base.metadata.drop_all(bind=engine)

# Add helper function for job fixture
@pytest.fixture
def test_job():
    return Job(
        id=1,
        title='Python Developer',
        description='Looking for a Python expert',
        required_skills=['python', 'django'],
        required_experience=2.0,
        required_education='bachelor',
        location='New York',
        remote_ok=True
    )

def test_search_jobs_basic():
    response = client.get("/search?search_text=python&user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "pagination" in data
    assert data["search_text"] == "python"
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 10

def test_search_jobs_pagination():
    # Test first page
    response = client.get("/search?search_text=python&user_id=1&page=1&page_size=2")
    data = response.json()
    assert len(data["recommendations"]) == 2
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 2
    assert data["pagination"]["total"] > 2

    # Test second page
    response = client.get("/search?search_text=python&user_id=1&page=2&page_size=2")
    data = response.json()
    assert len(data["recommendations"]) <= 2
    assert data["pagination"]["page"] == 2

def test_search_jobs_invalid_pagination():
    # Test invalid page number
    response = client.get("/search?search_text=python&user_id=1&page=0")
    assert response.status_code == 422

    # Test invalid page size
    response = client.get("/search?search_text=python&user_id=1&page_size=0")
    assert response.status_code == 422

def test_search_jobs_no_results():
    response = client.get("/search?search_text=nonexistentjob&user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "No jobs found"
    assert data["recommendations"] == []
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["total_pages"] == 0

def test_search_jobs_invalid_user():
    response = client.get("/search?search_text=python&user_id=999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_search_jobs_exact_match():
    response = client.get("/search?search_text=Python Developer&user_id=1")
    data = response.json()
    assert data["recommendations"][0]["job"]["title"] == "Python Developer"

def test_search_jobs_partial_match():
    response = client.get("/search?search_text=ML&user_id=1")
    data = response.json()
    assert any("ML" in job["job"]["title"] for job in data["recommendations"])

def test_search_jobs_case_insensitive():
    response = client.get("/search?search_text=PYTHON&user_id=1")
    data = response.json()
    assert len(data["recommendations"]) > 0


def test_recommend_candidates_basic():
    response = client.get("/recommend-candidates?job_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 10

def test_recommend_candidates_pagination():
    # Test first page
    response = client.get("/recommend-candidates?job_id=1&page=1&page_size=2")
    data = response.json()
    assert len(data["recommendations"]) <= 2
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 2

    # Test second page
    response = client.get("/recommend-candidates?job_id=1&page=2&page_size=2")
    data = response.json()
    assert len(data["recommendations"]) <= 2
    assert data["pagination"]["page"] == 2

def test_recommend_candidates_invalid_job(test_job):
    response = client.get("/recommend-candidates?job_id=999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

def test_recommend_candidates_skills_match(test_job):
    response = client.get("/recommend-candidates?job_id=1")
    data = response.json()
    # First candidate should have all required skills
    if data["recommendations"]:
        first_candidate = data["recommendations"][0]["candidate"]
        assert all(skill in first_candidate["skills"] for skill in test_job.required_skills)

def test_recommend_candidates_experience_match(test_job):
    response = client.get("/recommend-candidates?job_id=1")
    data = response.json()
    # First candidate should meet experience requirement
    if data["recommendations"]:
        first_candidate = data["recommendations"][0]["candidate"]
        assert first_candidate["experience"] >= test_job.required_experience