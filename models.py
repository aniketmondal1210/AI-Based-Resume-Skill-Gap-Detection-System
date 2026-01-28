from datetime import datetime
from database import db
import json

class AnalysisHistory:
    """Helper class to handle resume analysis history in MongoDB."""
    
    COLLECTION_NAME = 'analysis_history'

    @staticmethod
    def save(data):
        """Save analysis record to MongoDB."""
        record = {
            'timestamp': datetime.utcnow(),
            'job_role': data.get('job_role'),
            'match_percentage': data.get('match_percentage'),
            'readiness_score': data.get('readiness_score'),
            'semantic_summary': data.get('semantic_summary'),
            'ai_recommendations': data.get('ai_recommendations', []),
            'matched_skills': data.get('matched_skills', []),
            'missing_skills': data.get('missing_skills', []),
            'rating': data.get('rating'),
            'summary_message': data.get('summary_message'),
            'best_fit_role': data.get('best_fit_role'),
            'best_fit_reason': data.get('best_fit_reason')
        }
        return db[AnalysisHistory.COLLECTION_NAME].insert_one(record)

    @staticmethod
    def get_all(limit=10):
        """Retrieve recent analysis history."""
        cursor = db[AnalysisHistory.COLLECTION_NAME].find().sort('timestamp', -1).limit(limit)
        results = []
        for doc in cursor:
            doc['id'] = str(doc.pop('_id')) # Convert ObjectId to string
            if 'timestamp' in doc:
                doc['timestamp'] = doc['timestamp'].isoformat()
            results.append(doc)
        return results

    @staticmethod
    def to_dict(doc):
        """Helper to format a document for API response (similar to old model)."""
        if not doc:
            return None
        
        return {
            'id': str(doc.get('_id', '')),
            'timestamp': doc.get('timestamp').isoformat() if isinstance(doc.get('timestamp'), datetime) else doc.get('timestamp'),
            'job_role': doc.get('job_role'),
            'match_percentage': doc.get('match_percentage'),
            'readiness_score': doc.get('readiness_score'),
            'ai_insights': {
                'semantic_summary': doc.get('semantic_summary'),
                'curated_recommendations': doc.get('ai_recommendations', [])
            } if doc.get('semantic_summary') else None,
            'matched_skills': doc.get('matched_skills', []),
            'missing_skills': doc.get('missing_skills', []),
            'rating': doc.get('rating'),
            'message': doc.get('summary_message'),
            'best_fit': {
                'role': doc.get('best_fit_role'),
                'reason': doc.get('best_fit_reason')
            } if doc.get('best_fit_role') else None
        }
