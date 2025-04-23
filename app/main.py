from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, text
from app.database import get_db, engine
import app.models as models
from app.vectorizer import JobVectorizer
from app.recommender import JobRecommender
from app.logger import setup_logger
from app.candidate_recommender import CandidateRecommender
from app.utils import get_models_path

# Setup logger
logger = setup_logger()

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Initialize vectorizer and recommender
vectorizer = JobVectorizer()
# Update any vectorizer loading
vectorizer.load_vectorizer(get_models_path('job_vectorizer.pkl'))
recommender = JobRecommender(vectorizer)

app = FastAPI(
    title="Job Recommendation System",
    description="API for job recommendations",
    version="1.0.0"
)

@app.get("/search")
async def search_jobs(
    search_text: str,
    user_id: int,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    logger.info(f"Search request received - text: {search_text}, user_id: {user_id}, page: {page}")
    
    try:
        # Get the user
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            logger.warning(f"User not found - user_id: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Search jobs in database
        base_query = db.query(models.Job).filter(
            or_(
                models.Job.title.ilike(f"%{search_text}%"),
                models.Job.description.ilike(f"%{search_text}%")
            )
        )
        
        total_jobs = base_query.count()
        logger.info(f"Found {total_jobs} matching jobs")
        
        # Calculate pagination
        total_pages = (total_jobs + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        # Get paginated jobs
        jobs = base_query.offset(offset).limit(page_size).all()
        
        if not jobs:
            return {
                "message": "No jobs found",
                "recommendations": [],
                "pagination": {
                    "total": 0,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": 0
                }
            }
        
        # Get recommendations based on search results
        recommendations = recommender.get_recommendations(user, jobs, top_n=page_size)
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        return {
            "search_text": search_text,
            "recommendations": [
                {
                    "job": {
                        "id": job.id,
                        "title": job.title,
                        "description": job.description,
                        "required_skills": job.required_skills,
                        "required_experience": job.required_experience,
                        "required_education": job.required_education,
                        "location": job.location,
                        "remote_ok": job.remote_ok
                    },
                    "match_score": float(overall_score),
                    "similarity_score": float(similarity_score)
                }
                for job, overall_score, similarity_score in recommendations
            ],
            "pagination": {
                "total": total_jobs,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}", exc_info=True)
        raise

@app.get("/health")
async def health_check():
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        vectorizer_status = vectorizer.is_fitted()
        
        logger.info("Health check passed successfully")
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "database": "connected",
                "vectorizer": "ready" if vectorizer_status else "not ready",
                "version": "1.0.0"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

# Initialize candidate recommender
candidate_recommender = CandidateRecommender(vectorizer)

@app.get("/recommend-candidates")
async def recommend_candidates(
    job_id: int,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    try:
        # Get the job
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            logger.warning(f"Job not found - job_id: {job_id}")
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get all candidates
        candidates = db.query(models.User).all()
        
        # Get recommendations
        recommendations = candidate_recommender.get_recommendations(job, candidates, top_n=page_size)
        
        # Calculate pagination
        total_candidates = len(recommendations)
        total_pages = (total_candidates + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get paginated recommendations
        paginated_recommendations = recommendations[start_idx:end_idx]
        
        return {
            "recommendations": [
                {
                    "candidate": {
                        "id": candidate.id,
                        "skills": candidate.skills,
                        "experience": candidate.experience,
                        "education": candidate.education,
                        "location": candidate.location,
                        "remote_ok": candidate.remote_ok
                    },
                    "match_score": float(match_score),
                    "similarity_score": float(similarity_score)
                }
                for candidate, match_score, similarity_score in paginated_recommendations
            ],
            "pagination": {
                "total": total_candidates,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        }
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        logger.error(f"Error recommending candidates: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
