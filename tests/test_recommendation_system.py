import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorizer import JobVectorizer
from app.recommender import JobRecommender
from tests.utils.models import MockUser, MockJob
from app.utils import get_models_path

def test_recommendation_system():
    vectorizer = JobVectorizer()
    vectorizer.load_vectorizer(get_models_path('job_vectorizer.pkl'))
    
    # 2. Initialize recommender
    recommender = JobRecommender(vectorizer)
    
    # 3. Create test data
    test_user = MockUser(
        skills=['python', 'machine learning', 'sql', 'deep learning'],
        education=['bachelor, Computer Science', 'master, AI'],
        experience=3.5,
        location="New York, USA",
        remote_ok=True
    )
    
    test_jobs = [
        MockJob(
            title="Senior Data Scientist",
            description="Looking for an ML expert with Python and deep learning experience",
            required_skills=['python', 'machine learning', 'deep learning'],
            required_education='master',
            required_experience=5.0,
            location="New York, USA",
            remote_ok=True
        ),
        MockJob(  # Changed from TestJob
            title="Python Developer",
            description="Backend developer with SQL and Python experience needed",
            required_skills=['python', 'sql', 'django'],
            required_education='bachelor',
            required_experience=2.0,
            location="San Francisco, USA",
            remote_ok=False
        ),
        MockJob(  # Changed from TestJob
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
    recommendations = recommender.get_recommendations(test_user, test_jobs)
    
    # 5. Assertions
    assert len(recommendations) > 0
    assert all(isinstance(score, float) for _, score, _ in recommendations)
    assert all(score <= 1.0 for _, score, _ in recommendations)
    # Check if scores are in descending order
    scores = [score for _, score, _ in recommendations]
    assert all(scores[i] >= scores[i+1] for i in range(len(scores)-1))

if __name__ == "__main__":
    test_recommendation_system()