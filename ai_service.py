from google import genai
import os
import json
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Service to handle interactions with Google Gemini AI using the latest google-genai SDK."""
    
    def __init__(self, api_key):
        """Initialize Gemini with the provided API key."""
        if not api_key:
            logger.warning("Gemini API key not provided. AI features will be disabled.")
            self.client = None
            return
            
        try:
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-3-flash-preview'
        except Exception as e:
            logger.error(f"Error configuring Gemini: {str(e)}")
            self.client = None

    def analyze_resume(self, resume_text, job_role):
        """
        Send resume text and job role to Gemini for advanced analysis.
        Returns a dictionary with readiness score and curated recommendations.
        """
        if not self.client:
            return None

        prompt = f"""
        Analyze the following resume for the target job role: "{job_role}".
        
        STRICT EXTRACTION POLICY:
        1. Extract ONLY professional/technical skills and certifications that are EXPLICITLY mentioned in the resume.
        2. DO NOT hallucinate, infer, or assume skills that are not directly stated.
        3. If a candidate mentions "learning" or "interested in" a skill, do not count it as a possessed skill.
        
        Provide your analysis in the following JSON format:
        {{
            "readiness_score": (int from 0 to 100),
            "semantic_match_summary": "A brief summary of how well the candidate's experience matches the role semantically.",
            "curated_recommendations": [
                "A list of specific, actionable steps to bridge the gap for this role",
                "Include MUST-HAVE certifications for this specific role if the candidate lacks them",
                "Minimum 3 recommendations"
            ],
            "extracted_skills": [
                "A list of professional and technical skills and CERTIFICATIONS identified in the resume"
            ],
            "best_fit_role": "The job role that most accurately describes this candidate's profile based on their experience and skills",
            "best_fit_reason": "A brief explanation of why this candidate is a perfect fit for the best_fit_role"
        }}
        
        Resume Text:
        ---
        {resume_text}
        ---
        
        Important: Return ONLY the raw JSON object. Use double quotes for keys and string values.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if not response or not response.text:
                logger.error("Empty response from Gemini")
                return None

            response_text = response.text.strip()
            # Try to find JSON in the response if it's wrapped in backticks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Additional cleanup for potential stray characters
            if response_text.startswith('```'):
                response_text = response_text.replace('```', '')
                
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"Gemini analysis error: {str(e)}")
            return None
