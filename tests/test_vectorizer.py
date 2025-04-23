import pandas as pd
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorizer import JobVectorizer
from dataclasses import dataclass

# Create mock data classes to simulate our database models
@dataclass
class MockJob:
    title: str
    description: str
    required_skills: list
    required_education: str

@dataclass
class MockUser:
    skills: list
    education: list

def main():
    # 1. Create and train vectorizer
    print("Creating and training vectorizer...")
    vectorizer = JobVectorizer()
    
    # Load sample jobs data
    df = pd.read_csv('d:/studies/AI/job_recommendation_system/data/linkedin_jobs.csv')
    
    # Create mock jobs for training
    jobs = [
        MockJob(
            title=row['title'],
            description=row['description'],
            required_skills=['python', 'sql'] if pd.notna(row['skills_desc']) else [],
            required_education='bachelor'
        )
        for _, row in df.head(1000).iterrows()  # Using first 1000 jobs for this example
    ]
    
    # Fit vectorizer
    vectorizer.fit(jobs)
    print("Vectorizer trained successfully!")
    
    # 2. Save the trained vectorizer
    save_path = 'd:/studies/AI/job_recommendation_system/models/job_vectorizer.pkl'
    vectorizer.save_vectorizer(save_path)
    print(f"Vectorizer saved to {save_path}")
    
    # 3. Load the vectorizer in a new instance
    print("\nLoading saved vectorizer...")
    new_vectorizer = JobVectorizer()
    new_vectorizer.load_vectorizer(save_path)
    print("Vectorizer loaded successfully!")
    
    # 4. Test the loaded vectorizer
    print("\nTesting vectorizer with sample data...")
    
    # Create a sample user
    test_user = MockUser(
        skills=['python', 'machine learning', 'data analysis'],
        education=['bachelor, Computer Science', 'master, Data Science']
    )
    
    # Create a sample job
    test_job = MockJob(
        title="Data Scientist",
        description="Looking for a Python expert with ML skills",
        required_skills=['python', 'machine learning'],
        required_education='master'
    )
    
    # Transform user and job
    user_vector = new_vectorizer.transform_user(test_user)
    job_vector = new_vectorizer.transform_job(test_job)
    
    print("\nVectorization successful!")
    print(f"User vector shape: {user_vector.shape}")
    print(f"Job vector shape: {job_vector.shape}")
    
    # Verify vectorizer is fitted
    print(f"\nVectorizer is fitted: {new_vectorizer.is_fitted()}")

if __name__ == "__main__":
    main()