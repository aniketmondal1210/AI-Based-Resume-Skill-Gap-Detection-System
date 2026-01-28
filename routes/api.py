from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
from skill_analyzer import SkillAnalyzer
from database import db
from models import AnalysisHistory
import PyPDF2
import docx

api_bp = Blueprint('api', __name__)
_skill_analyzer = None

def get_analyzer():
    global _skill_analyzer
    if _skill_analyzer is None:
        api_key = current_app.config.get('GEMINI_API_KEY')
        _skill_analyzer = SkillAnalyzer(api_key=api_key)
    return _skill_analyzer

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(filepath):
    """Extract text based on file extension."""
    ext = filepath.rsplit('.', 1)[1].lower()
    try:
        if ext == 'pdf':
            text = ""
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        elif ext == 'docx':
            doc = docx.Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        current_app.logger.error(f"Text extraction error: {str(e)}")
        return None
    return None

@api_bp.route('/job-roles', methods=['GET'])
def get_job_roles():
    return jsonify({'roles': get_analyzer().get_available_roles()})

@api_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        resume_text = None
        job_role = request.form.get('job_role')
        
        if not job_role:
            return jsonify({'error': 'Please select a job role'}), 400

        # Handle text input
        if 'resume_text' in request.form and request.form['resume_text'].strip():
            resume_text = request.form['resume_text']
        
        # Handle file upload
        elif 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                resume_text = extract_text_from_file(filepath)
                
                # Cleanup
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                if not resume_text:
                    return jsonify({'error': 'Failed to extract text from file'}), 400
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        else:
            return jsonify({'error': 'No resume provided'}), 400

        # Analysis
        analyzer = get_analyzer()
        result = analyzer.analyze(resume_text, job_role)
        if 'error' in result:
            return jsonify(result), 400

        # Save to History
        history_data = {
            'job_role': job_role,
            'match_percentage': result['match_percentage'],
            'readiness_score': result.get('readiness_score'),
            'matched_skills': result['matched_skills'],
            'missing_skills': result['missing_skills'],
            'rating': result['analysis_summary']['rating'],
            'summary_message': result['analysis_summary']['message'],
            'best_fit_role': result.get('ai_insights', {}).get('best_fit_role'),
            'best_fit_reason': result.get('ai_insights', {}).get('best_fit_reason')
        }
        
        # Add AI insights if they exist
        if result.get('ai_insights'):
            history_data['semantic_summary'] = result['ai_insights']['semantic_summary']
            history_data['ai_recommendations'] = result['ai_insights']['curated_recommendations']
            
        save_result = AnalysisHistory.save(history_data)

        # Add history ID to result
        result['history_id'] = str(save_result.inserted_id)

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': 'An internal error occurred during analysis'}), 500

@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get analysis history for dashboard."""
    limit = request.args.get('limit', 10, type=int)
    history = AnalysisHistory.get_all(limit=limit)
    return jsonify(history)
