from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models import Job  # Add this import

class CandidateRecommender:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def _calculate_content_similarity(self, job, candidates):
        if not candidates:
            return np.array([])
            
        # Transform job text
        job_vector = self.vectorizer.transform_job(job)
        
        # Transform candidate texts
        candidate_vectors = []
        for candidate in candidates:
            # Create a Job object from candidate data
            candidate_job = Job(
                id=candidate.id,
                title=' '.join(candidate.skills),
                description=' '.join(candidate.education),
                required_skills=candidate.skills,
                required_education=candidate.education[0] if candidate.education else '',
                required_experience=candidate.experience,
                location=candidate.location,
                remote_ok=candidate.remote_ok
            )
            candidate_vectors.append(self.vectorizer.transform_job(candidate_job))
        
        # Stack all candidate vectors
        candidate_vectors = np.vstack(candidate_vectors)
        
        # Calculate similarity between job and each candidate
        similarities = cosine_similarity(candidate_vectors, job_vector.reshape(1, -1)).flatten()
        return similarities

    def _calculate_experience_match(self, job, candidates):
        scores = []
        for candidate in candidates:
            if candidate.experience >= job.required_experience:
                # Give bonus points for experience up to 2 years over requirement
                extra_exp = min(candidate.experience - job.required_experience, 2.0)
                score = 1.0 + (extra_exp / 4.0)  # Max score is 1.5
            else:
                # Penalize missing experience
                missing_exp = job.required_experience - candidate.experience
                score = max(0.0, 1.0 - (missing_exp / job.required_experience))
            scores.append(score)
        return np.array(scores)

    def _calculate_education_match(self, job, candidates):
        scores = []
        for candidate in candidates:
            if self._meets_education_requirement(job.required_education, candidate.education):
                scores.append(1.0)
            else:
                scores.append(0.0)
        return np.array(scores)

    def _meets_education_requirement(self, required_education, candidate_education):
        education_levels = {
            'high school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5
        }
        
        required_level = education_levels.get(required_education.lower(), 0)
        
        # Check if any of candidate's education meets or exceeds requirement
        for edu in candidate_education:
            edu_parts = edu.lower().split(',')
            if edu_parts:
                level = edu_parts[0].strip()
                if education_levels.get(level, 0) >= required_level:
                    return True
        return False

    def get_recommendations(self, job, candidates, top_n=10):
        # Content similarity (40% of score)
        content_score = self._calculate_content_similarity(job, candidates)
        
        # Required skills match (30% of score)
        skills_score = self._calculate_skills_match(job, candidates)
        
        # Experience match (20% of score)
        experience_score = self._calculate_experience_match(job, candidates)
        
        # Education match (10% of score)
        education_score = self._calculate_education_match(job, candidates)
        
        # Calculate weighted score
        overall_scores = (
            0.4 * content_score +
            0.3 * skills_score +
            0.2 * experience_score +
            0.1 * education_score
        )
        
        # Filter out candidates that don't meet minimum requirements
        mask = self._apply_hard_requirements(job, candidates)
        overall_scores[~mask] = -1
        
        # Get top candidates
        top_indices = np.argsort(overall_scores)[::-1][:top_n]
        
        return [
            (candidates[i], overall_scores[i], content_score[i])
            for i in top_indices if overall_scores[i] > 0
        ]

    def _apply_hard_requirements(self, job, candidates):
        mask = np.ones(len(candidates), dtype=bool)
        for i, candidate in enumerate(candidates):
            # Must have minimum experience
            if candidate.experience < job.required_experience:
                mask[i] = False
            # Must have required education level
            if not self._meets_education_requirement(job.required_education, candidate.education):
                mask[i] = False
            # Must have all essential skills
            if not all(skill in candidate.skills for skill in job.required_skills):
                mask[i] = False
        return mask

    def _calculate_skills_match(self, job, candidates):
        scores = []
        required_skills = set(job.required_skills)
        for candidate in candidates:
            candidate_skills = set(candidate.skills)
            if required_skills:
                score = len(required_skills.intersection(candidate_skills)) / len(required_skills)
            else:
                score = 0
            scores.append(score)
        return np.array(scores)