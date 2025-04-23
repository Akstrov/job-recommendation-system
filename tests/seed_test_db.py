import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Job

# Test database configuration
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_test_database():
    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Clear existing data
    db.query(Job).delete()
    db.query(User).delete()
    db.commit()
    
    # Create mock users
    users = [
        User(
            id=1,
            skills=['python', 'django', 'react', 'postgresql'],
            experience=5.0,
            education=['master, Computer Science'],
            location='New York',
            remote_ok=True
        ),
        User(
            id=2,
            skills=['python', 'machine learning', 'tensorflow', 'pytorch'],
            experience=3.0,
            education=['phd, Data Science'],
            location='San Francisco',
            remote_ok=False
        ),
        User(
            id=3,
            skills=['java', 'spring', 'kubernetes', 'microservices'],
            experience=7.0,
            education=['bachelor, Software Engineering'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=4,
            skills=['python', 'fastapi', 'mongodb', 'aws'],
            experience=4.0,
            education=['master, Software Engineering'],
            location='Boston',
            remote_ok=True
        ),
        User(
            id=5,
            skills=['javascript', 'react', 'node.js', 'typescript'],
            experience=3.0,
            education=['bachelor, Computer Science'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=6,
            skills=['python', 'data science', 'sql', 'tableau', 'r'],
            experience=4.0,
            education=['master, Data Analytics'],
            location='Chicago',
            remote_ok=True
        ),
        User(
            id=7,
            skills=['java', 'spring boot', 'mysql', 'docker', 'aws'],
            experience=6.0,
            education=['master, Software Engineering'],
            location='Seattle',
            remote_ok=True
        ),
        User(
            id=8,
            skills=['python', 'django', 'react', 'aws', 'docker'],
            experience=3.5,
            education=['bachelor, Computer Engineering'],
            location='Austin',
            remote_ok=True
        ),
        User(
            id=9,
            skills=['javascript', 'vue.js', 'node.js', 'mongodb', 'graphql'],
            experience=4.5,
            education=['bachelor, Web Development'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=10,
            skills=['python', 'tensorflow', 'keras', 'computer vision', 'deep learning'],
            experience=5.0,
            education=['phd, Computer Vision'],
            location='Boston',
            remote_ok=False
        ),
        User(
            id=11,
            skills=['java', 'kotlin', 'android', 'firebase', 'mobile development'],
            experience=4.0,
            education=['bachelor, Mobile Development'],
            location='San Francisco',
            remote_ok=False
        ),
        User(
            id=12,
            skills=['python', 'nlp', 'bert', 'transformers', 'machine learning'],
            experience=3.0,
            education=['master, Natural Language Processing'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=13,
            skills=['c++', 'cuda', 'opencv', 'robotics', 'ros'],
            experience=6.0,
            education=['phd, Robotics'],
            location='Pittsburgh',
            remote_ok=False
        ),
        User(
            id=14,
            skills=['rust', 'golang', 'kubernetes', 'microservices', 'devops'],
            experience=5.0,
            education=['master, Cloud Computing'],
            location='Remote',
            remote_ok=True
        ),
        User(
            id=15,
            skills=['swift', 'ios', 'objective-c', 'mobile development', 'xcode'],
            experience=4.0,
            education=['bachelor, Mobile Development'],
            location='New York',
            remote_ok=False
        )
    ]
    
    # Create mock jobs
    jobs = [
        Job(
            id=1,
            title='Senior Python Developer',
            description='Looking for an experienced Python developer with Django expertise',
            required_skills=['python', 'django', 'postgresql'],
            required_experience=4.0,
            required_education='bachelor',
            location='New York',
            remote_ok=True
        ),
        Job(
            id=2,
            title='Machine Learning Engineer',
            description='AI/ML position for computer vision projects',
            required_skills=['python', 'machine learning', 'tensorflow'],
            required_experience=2.0,
            required_education='master',
            location='San Francisco',
            remote_ok=False
        ),
        Job(
            id=3,
            title='Backend Developer',
            description='Java backend developer for microservices architecture',
            required_skills=['java', 'spring', 'kubernetes'],
            required_experience=5.0,
            required_education='bachelor',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=4,
            title='Full Stack Developer',
            description='Full stack developer with React and Node.js experience',
            required_skills=['javascript', 'react', 'node.js'],
            required_experience=3.0,
            required_education='bachelor',
            location='Boston',
            remote_ok=True
        ),
        Job(
            id=5,
            title='Python API Developer',
            description='FastAPI developer for building scalable APIs',
            required_skills=['python', 'fastapi', 'mongodb'],
            required_experience=2.0,
            required_education='bachelor',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=6,
            title='Data Scientist',
            description='Looking for a data scientist with strong Python and R skills',
            required_skills=['python', 'r', 'sql', 'machine learning'],
            required_experience=3.0,
            required_education='master',
            location='Chicago',
            remote_ok=True
        ),
        Job(
            id=7,
            title='Senior Java Developer',
            description='Enterprise Java developer with Spring Boot expertise',
            required_skills=['java', 'spring boot', 'mysql', 'docker'],
            required_experience=5.0,
            required_education='bachelor',
            location='Seattle',
            remote_ok=True
        ),
        Job(
            id=8,
            title='Full Stack Python Developer',
            description='Full stack developer with Django and React experience',
            required_skills=['python', 'django', 'react', 'aws'],
            required_experience=3.0,
            required_education='bachelor',
            location='Austin',
            remote_ok=True
        ),
        Job(
            id=9,
            title='Computer Vision Engineer',
            description='Deep learning engineer for computer vision projects',
            required_skills=['python', 'tensorflow', 'computer vision', 'deep learning'],
            required_experience=4.0,
            required_education='phd',
            location='Boston',
            remote_ok=False
        ),
        Job(
            id=10,
            title='Mobile Developer',
            description='Android developer with Kotlin experience',
            required_skills=['java', 'kotlin', 'android', 'mobile development'],
            required_experience=3.0,
            required_education='bachelor',
            location='San Francisco',
            remote_ok=False
        ),
        Job(
            id=11,
            title='NLP Engineer',
            description='NLP engineer for transformer-based models',
            required_skills=['python', 'nlp', 'bert', 'machine learning'],
            required_experience=2.0,
            required_education='master',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=12,
            title='Robotics Engineer',
            description='C++ developer for robotics software',
            required_skills=['c++', 'opencv', 'robotics', 'ros'],
            required_experience=5.0,
            required_education='phd',
            location='Pittsburgh',
            remote_ok=False
        ),
        Job(
            id=13,
            title='DevOps Engineer',
            description='Cloud native developer with Kubernetes expertise',
            required_skills=['golang', 'kubernetes', 'microservices', 'devops'],
            required_experience=4.0,
            required_education='master',
            location='Remote',
            remote_ok=True
        ),
        Job(
            id=14,
            title='iOS Developer',
            description='Senior iOS developer with Swift expertise',
            required_skills=['swift', 'ios', 'mobile development', 'xcode'],
            required_experience=3.0,
            required_education='bachelor',
            location='New York',
            remote_ok=False
        ),
        Job(
            id=15,
            title='Backend Go Developer',
            description='Golang developer for high-performance services',
            required_skills=['golang', 'microservices', 'kubernetes', 'docker'],
            required_experience=4.0,
            required_education='bachelor',
            location='Remote',
            remote_ok=True
        )
    ]
    
    # Add to database
    db.add_all(users)
    db.add_all(jobs)
    db.commit()

    # Verify data was added
    job_count = db.query(Job).count()
    user_count = db.query(User).count()
    print(f"Seeded database with {job_count} jobs and {user_count} users")
    
    # Verify specific job exists
    job3 = db.query(Job).filter(Job.id == 3).first()
    if job3:
        print(f"Job #3 exists: {job3.title}")
    else:
        print("Warning: Job #3 not found after seeding")
    
    db.close()

if __name__ == "__main__":
    seed_test_database()