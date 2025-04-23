# Job Recommendation System

A machine learning-based system that matches jobs with candidates and vice versa using content-based filtering and similarity scoring.

## Features

- Job-to-Candidate matching
- Candidate-to-Job matching
- Content-based recommendation using TF-IDF vectorization
- Multi-factor scoring system including:
  - Skills matching
  - Experience level matching
  - Education requirements
  - Location preferences
  - Remote work compatibility

## Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy
- scikit-learn
- NumPy
- PostgreSQL
- pytest

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
    python -m venv venv
```
3. Activate the virtual environment:
```bash
    .\venv\Scripts\activate
```
4. Install dependencies:
```bash
    pip install -r requirements.txt
```
## Project Structure

    job_recommendation_system/
    ├── app/                    # Main application code
    │   ├── candidate_recommender.py
    │   ├── recommender.py
    │   ├── vectorizer.py
    │   └── models.py
    ├── data/                   # Data files
    │   └── Linkedin_jobs.csv
    ├── models/                 # Trained ML models
    │   └── job_vectorizer.pkl
    ├── tests/                  # Test files
    ├── scripts/               # Utility scripts
    └── requirements.txt

## Usage

1. Train the vectorizer:
```bash
    python scripts/train_vectorizer.py
```
2. Run the tests:
```bash
    pytest .\tests\
```
## Recommendation System Details

The system uses a combination of:
- TF-IDF vectorization for content similarity
- Hard requirement filtering
- Weighted scoring system:
  - Content similarity (40%)
  - Required skills match (30%)
  - Experience match (20%)
  - Education match (10%)

## Testing

The project includes comprehensive test coverage for:
- Recommendation algorithms
- Candidate matching
- Job matching
- Vectorizer functionality
- API endpoints

Run tests using:
```bash
    pytest .\tests\
```