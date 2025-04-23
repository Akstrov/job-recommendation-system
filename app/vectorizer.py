import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class JobVectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Reduced from 1000
            stop_words='english',
            ngram_range=(1, 1),  # Changed from (1,2) to reduce memory usage
            min_df=10,  # Increased from 5
            max_df=0.90,  # Slightly reduced
            dtype=np.float32  # Use float32 instead of float64 to save memory
        )
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess_text(self, text):
        try:
            # Convert to lowercase
            text = str(text).lower()
            
            # Remove special characters and numbers
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words]
            
            # POS tagging and lemmatization
            pos_tags = nltk.pos_tag(tokens)
            lemmatized_tokens = []
            for token, tag in pos_tags:
                if tag.startswith('VB'):
                    lem_token = self.lemmatizer.lemmatize(token, pos='v')
                elif tag.startswith('NN'):
                    lem_token = self.lemmatizer.lemmatize(token, pos='n')
                elif tag.startswith('JJ'):
                    lem_token = self.lemmatizer.lemmatize(token, pos='a')
                else:
                    lem_token = self.lemmatizer.lemmatize(token)
                lemmatized_tokens.append(lem_token)
            
            return ' '.join(lemmatized_tokens)
        except Exception as e:
            print(f"Error processing text: {e}")
            return ''

    def prepare_combined_text(self, text_parts):
        combined_text = ' | '.join(filter(None, text_parts))
        return self.preprocess_text(combined_text)

    def prepare_user_text(self, user):
        text_parts = [
            ' '.join(user.skills) if user.skills else '',
            ' '.join(user.education) if user.education else '',
            str(user.experience) + ' years experience',
            user.location if user.location else ''
        ]
        return self.prepare_combined_text(text_parts)

    def prepare_job_text(self, job):
        text_parts = [
            job.title if job.title else '',
            job.description if job.description else '',
            ' '.join(job.required_skills) if job.required_skills else '',
            job.required_education if job.required_education else '',
            str(job.required_experience) + ' years required',
            job.location if job.location else ''
        ]
        return self.prepare_combined_text(text_parts)

    def fit(self, jobs):
        job_texts = [self.prepare_job_text(job) for job in jobs]
        self.vectorizer.fit(job_texts)
    
    def transform_user(self, user):
        user_text = self.prepare_user_text(user)
        return self.vectorizer.transform([user_text]).toarray()[0]
    
    def transform_job(self, job):
        job_text = self.prepare_job_text(job)
        return self.vectorizer.transform([job_text]).toarray()[0]
    
    def save_vectorizer(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_vectorizer(self, path):
        with open(path, 'rb') as f:
            self.vectorizer = pickle.load(f)

    def is_fitted(self):
        try:
            # Check if vocabulary exists
            _ = self.vectorizer.vocabulary_
            return True
        except:
            return False