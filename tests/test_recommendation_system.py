import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorizer import JobVectorizer
from app.recommender import JobRecommender
from dataclasses import dataclass

@dataclass
class TestUser:
    skills: list
    education: list
    experience: float
    location: str
    remote_ok: bool

@dataclass
class TestJob:
    title: str
    description: str
    required_skills: list
    required_education: str
    required_experience: float
    location: str
    remote_ok: bool

def main():
    # 1. Load the trained vectorizer
    print("Loading vectorizer...")
    vectorizer = JobVectorizer()
    vectorizer.load_vectorizer('d:/studies/AI/job_recommendation_system/models/job_vectorizer.pkl')
    
    # 2. Initialize recommender
    recommender = JobRecommender(vectorizer)
    
    # 3. Create test data
    test_user = TestUser(
        skills=['python', 'machine learning', 'sql', 'deep learning'],
        education=['bachelor, Computer Science', 'master, AI'],
        experience=3.5,
        location="New York, USA",
        remote_ok=True
    )
    
    test_jobs = [
        TestJob(
            title="Senior Data Scientist",
            description="Looking for an ML expert with Python and deep learning experience",
            required_skills=['python', 'machine learning', 'deep learning'],
            required_education='master',
            required_experience=5.0,
            location="New York, USA",
            remote_ok=True
        ),
        TestJob(
            title="Python Developer",
            description="Backend developer with SQL and Python experience needed",
            required_skills=['python', 'sql', 'django'],
            required_education='bachelor',
            required_experience=2.0,
            location="San Francisco, USA",
            remote_ok=False
        ),
        TestJob(
            title="ML Engineer",
            description="AI startup seeking ML engineer with deep learning expertise",
            required_skills=['python', 'machine learning', 'tensorflow'],
            required_education='master',
            required_experience=3.0,
            location="Remote",
            remote_ok=True
        )
    ]
    
    # 4. Get recommendations
    print("\nGetting recommendations for user...")
    recommendations = recommender.get_recommendations(test_user, test_jobs)
    
    # 5. Display results
    print("\nTop recommendations:")
    for job, overall_score, similarity_score in recommendations:
        print(f"\nJob: {job.title}")
        print(f"Overall Match Score: {overall_score:.4f}")
        print(f"Content Similarity: {similarity_score:.4f}")
        print(f"Location: {job.location}")
        print(f"Required Experience: {job.required_experience} years")
        print(f"Required Education: {job.required_education}")
        print(f"Remote OK: {job.remote_ok}")

if __name__ == "__main__":
    main()