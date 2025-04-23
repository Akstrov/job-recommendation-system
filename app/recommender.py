from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .vectorizer import JobVectorizer

class JobRecommender:
    def __init__(self, vectorizer: JobVectorizer):
        self.vectorizer = vectorizer

    def calculate_match_score(self, user, job, similarity_score):
        # Base score from TFIDF similarity (60% weight)
        total_score = similarity_score * 0.6

        # Experience match (20% weight)
        exp_score = 0.0
        if user.experience >= job.required_experience:
            exp_score = 0.2
        elif user.experience >= job.required_experience * 0.8:
            exp_score = 0.1
        total_score += exp_score

        # Location match (10% weight)
        location_score = 0.1 if (user.location == job.location or 
                               (job.remote_ok and user.remote_ok)) else 0.0
        total_score += location_score

        # Education match (10% weight)
        education_levels = {'high school': 1, 'bachelor': 2, 'master': 3, 'phd': 4}
        user_highest_edu = max([education_levels.get(edu.split(',')[0].strip().lower(), 0) 
                              for edu in user.education])
        required_edu = education_levels.get(job.required_education.lower(), 0)
        education_score = 0.1 if user_highest_edu >= required_edu else 0.0
        total_score += education_score

        return total_score

    def get_recommendations(self, user, jobs, top_n=10):
        user_vector = self.vectorizer.transform_user(user)
        job_vectors = np.vstack([self.vectorizer.transform_job(job) for job in jobs])
        
        similarities = cosine_similarity([user_vector], job_vectors)[0]
        
        job_scores = []
        for job, sim_score in zip(jobs, similarities):
            overall_score = self.calculate_match_score(user, job, sim_score)
            job_scores.append((job, overall_score, sim_score))
        
        return sorted(job_scores, key=lambda x: x[1], reverse=True)[:top_n]