import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vectorizer import JobVectorizer

def train_vectorizer():
    # Load the LinkedIn jobs dataset
    df = pd.read_csv('d:/studies/AI/job_recommendation_system/data/linkedin_jobs.csv')
    
    # Select relevant columns and clean data
    df_clean = df[['title', 'description']].dropna(subset=['description'])
    
    # Take a random sample to reduce memory usage
    sample_size = 50000  # Adjust this number based on your memory constraints
    df_sample = df_clean.sample(n=min(sample_size, len(df_clean)), random_state=42)
    
    # Create mock jobs
    class MockJob:
        def __init__(self, title, description):
            self.title = title
            self.description = description
            self.required_skills = []
            self.required_experience = 0
            self.required_education = ''
            self.location = ''
    
    # Convert DataFrame rows to MockJob objects
    mock_jobs = [MockJob(row['title'], row['description']) for _, row in df_sample.iterrows()]
    
    print(f"Training vectorizer with {len(mock_jobs)} job descriptions...")
    
    # Initialize and train vectorizer
    vectorizer = JobVectorizer()
    vectorizer.fit(mock_jobs)
    
    # Save the trained vectorizer
    model_path = 'd:/studies/AI/job_recommendation_system/models/job_vectorizer.pkl'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    vectorizer.save_vectorizer(model_path)
    print(f"Vectorizer trained and saved to {model_path}")

if __name__ == "__main__":
    train_vectorizer()