import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import User, Job, Base
from app.database import SessionLocal, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

def test_database():
    db = SessionLocal()
    try:
        # Create sample user
        test_user = User(
            skills=["Python", "FastAPI", "SQL", "Machine Learning"],
            experience=5.5,
            education=[
                "bachelor, University of Technology",
                "master, Institute of Higher Technology of Rabat"
            ],
            location="Rabat, Morocco",
            remote_ok=True,
            tfidf_vector=[0.5, 0.3, 0.2]  # Sample vector
        )

        # Create sample job
        test_job = Job(
            title="Senior ML Engineer",
            description="Looking for an experienced ML engineer...",
            required_skills=["Python", "TensorFlow", "SQL"],
            required_experience=4.0,
            required_education="master",
            location="Casablanca, Morocco",
            remote_ok=True,
            tfidf_vector=[0.4, 0.3, 0.3]  # Sample vector
        )

        # Add to database
        db.add(test_user)
        db.add(test_job)
        db.commit()

        # Verify data
        users = db.query(User).all()
        jobs = db.query(Job).all()

        print("\n=== Users in Database ===")
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"Skills: {user.skills}")
            print(f"Experience: {user.experience} years")
            print(f"Education: {user.education}")
            print(f"Location: {user.location}")
            print(f"Remote OK: {user.remote_ok}")

        print("\n=== Jobs in Database ===")
        for job in jobs:
            print(f"\nJob ID: {job.id}")
            print(f"Title: {job.title}")
            print(f"Required Skills: {job.required_skills}")
            print(f"Required Experience: {job.required_experience} years")
            print(f"Required Education: {job.required_education}")
            print(f"Location: {job.location}")
            print(f"Remote OK: {job.remote_ok}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database()