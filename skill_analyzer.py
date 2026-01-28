"""
Advanced Skill Analyzer Module (Production Version)
Uses spaCy Matcher and Lemmatization for high-precision skill extraction.
"""

import re
import spacy
from spacy.matcher import Matcher
from ai_service import AIService

class SkillAnalyzer:
    """
    Analyzes resumes using NLP patterns and rule-based matching.
    """
    
    def __init__(self, api_key=None, model_name="en_core_web_sm"):
        """Initialize NLP, AI Service, and Predefined skill sets."""
        self.ai_service = AIService(api_key) if api_key else None
        try:
            self.nlp = spacy.load(model_name)
        except:
            print(f"Error: spaCy model {model_name} not found. Using fallback matching.")
            self.nlp = None
            
        self.matcher = Matcher(self.nlp.vocab) if self.nlp else None
        
        # Predefined skill sets (Extensively Curated for Production)
        self.job_skills = {
            'Software Engineer': {
                'programming_languages': ['Python', 'Java', 'C++', 'JavaScript', 'TypeScript', 'C#', 'Ruby', 'Go', 'Rust', 'PHP'],
                'frameworks': ['React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring Boot', 'Node.js', 'Express.js', 'FastAPI'],
                'databases': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle'],
                'tools': ['Git', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible', 'AWS', 'Azure', 'GCP'],
                'concepts': ['OOP', 'Data Structures', 'Algorithms', 'Design Patterns', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'TDD'],
                'certifications': ['AWS Certified Developer', 'Azure Developer Associate', 'Google Cloud Professional Developer', 'Oracle Certified Professional Java SE Developer']
            },
            'Data Engineer': {
                'programming_languages': ['Python', 'SQL', 'Scala', 'Java'],
                'tools': ['Apache Spark', 'Apache Kafka', 'Hadoop', 'Airflow', 'dbt', 'Snowflake', 'BigQuery', 'Redshift', 'Databricks'],
                'databases': ['PostgreSQL', 'MongoDB', 'Cassandra', 'Redis'],
                'concepts': ['ETL', 'Data Pipeline', 'Data Warehouse', 'Data Lake', 'Data Modeling', 'Data Governance', 'Distributed Systems'],
                'certifications': ['Google Professional Data Engineer', 'AWS Certified Data Analytics', 'Azure Data Engineer Associate', 'Cloudera Certified Professional Data Engineer']
            },
            'Data Scientist': {
                'programming_languages': ['Python', 'R', 'SQL', 'Scala'],
                'libraries': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras', 'XGBoost', 'Matplotlib', 'Seaborn'],
                'tools': ['Jupyter', 'Tableau', 'Power BI', 'MLflow', 'DVC'],
                'concepts': ['Machine Learning', 'Deep Learning', 'Statistics', 'NLP', 'Computer Vision', 'Data Mining', 'Feature Engineering'],
                'certifications': ['Certified Analytics Professional (CAP)', 'Google Professional Data Scientist', 'Azure Data Scientist Associate']
            },
            'Data Analyst': {
                'programming_languages': ['Python', 'SQL', 'R'],
                'tools': ['Excel', 'Tableau', 'Power BI', 'Looker', 'SAS', 'Google Analytics'],
                'libraries': ['Pandas', 'NumPy', 'SciPy', 'Matplotlib'],
                'concepts': ['Data Visualization', 'ETL', 'Statistical Modeling', 'Business Intelligence', 'Data Cleaning', 'A/B Testing'],
                'certifications': ['Google Data Analytics Professional Certificate', 'Microsoft Certified: Power BI Data Analyst Associate', 'Tableau Desktop Specialist']
            },
            'DevOps Engineer': {
                'programming_languages': ['Python', 'Bash', 'Go', 'YAML'],
                'tools': ['Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible', 'Puppet', 'Chef', 'GitLab CI', 'Prometheus', 'Grafana'],
                'cloud_platforms': ['AWS', 'Azure', 'GCP'],
                'concepts': ['Infrastructure as Code', 'CI/CD Pipelines', 'Cloud Computing', 'Monitoring', 'Automation', 'Site Reliability Engineering'],
                'certifications': ['AWS Certified DevOps Engineer', 'Azure DevOps Engineer Expert', 'Certified Kubernetes Administrator (CKA)']
            },
            'Cybersecurity Analyst': {
                'tools': ['Wireshark', 'Metasploit', 'Nmap', 'Burp Suite', 'Splunk', 'SIEM', 'CrowdStrike', 'Nessus'],
                'concepts': ['Network Security', 'Penetration Testing', 'Incident Response', 'Vulnerability Management', 'IAM', 'Encryption', 'SOC'],
                'certifications': ['CompTIA Security+', 'CISSP', 'CEH (Certified Ethical Hacker)', 'CISM', 'CompTIA CySA+']
            },
            'AI Engineer': {
                'programming_languages': ['Python', 'C++', 'Java'],
                'libraries': ['TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'Hugging Face'],
                'concepts': ['Generative AI', 'LLMs', 'Neural Networks', 'Reinforcement Learning', 'NLP', 'Machine Learning Operations (MLOps)'],
                'certifications': ['Google Professional Machine Learning Engineer', 'Azure AI Engineer Associate', 'AWS Certified Machine Learning']
            },
            'Network Concentration Engineer': {
                'tools': ['Cisco IOS', 'Juniper', 'Wireshark', 'SolarWinds', 'Netflow'],
                'protocols': ['TCP/IP', 'BGP', 'OSPF', 'VLAN', 'MPLS', 'DNS', 'DHCP'],
                'concepts': ['Routing', 'Switching', 'Network Architecture', 'Load Balancing', 'Firewalls', 'VPN'],
                'certifications': ['CCNA', 'CCNP', 'JNCIA', 'JNCIS', 'CompTIA Network+']
            },
            'Systems Programmer': {
                'programming_languages': ['C', 'C++', 'Assembly', 'Rust', 'Go'],
                'concepts': ['Kernel Development', 'Operating Systems', 'Memory Management', 'Multithreading', 'Low-level I/O', 'Device Drivers'],
                'tools': ['GDB', 'Valgrind', 'Make', 'GCC', 'LLVM'],
                'certifications': ['Linux Foundation Certified System Administrator (LFCS)', 'Red Hat Certified Engineer (RHCE)']
            },
            'Digital Hardware Engineer': {
                'languages': ['Verilog', 'VHDL', 'SystemVerilog'],
                'tools': ['Vivado', 'Quartus', 'Cadence', 'Synopsys', 'ModelSim'],
                'concepts': ['FPGA Design', 'ASIC', 'Digital Logic', 'Computer Architecture', 'RTL Design', 'PCB Design'],
                'certifications': ['Professional Engineer (PE) License', 'IEEE Hardware Certifications']
            },
            'Computer Hardware Engineer': {
                'skills': ['Circuit Design', 'Embedded Systems', 'Microprocessors', 'Electronic Testing', 'Motherboard Design'],
                'tools': ['Altium Designer', 'Multisim', 'Orcad', 'Oscilloscopes', 'Spectrum Analyzers'],
                'concepts': ['VLSI', 'Solid State Physics', 'Signal Integrity', 'Thermal Management'],
                'certifications': ['CompTIA A+', 'CompTIA IT Fundamentals']
            },
            'Digital Signal Processor': {
                'programming_languages': ['MATLAB', 'C', 'Python'],
                'concepts': ['FFT', 'Filtering', 'Image Processing', 'Audio Processing', 'Modulation', 'Signal Analysis', 'Control Systems'],
                'tools': ['Simulink', 'LabVIEW', 'DSP Processors (TI/Analog Devices)'],
                'certifications': ['IEEE Signal Processing Society Certifications']
            },
            'Networks Engineer': {
                'tools': ['Cisco Webex', 'F5 Networks', 'Check Point', 'Palo Alto Networks'],
                'concepts': ['Software Defined Networking (SDN)', 'Network Function Virtualization (NFV)', '5G', 'SD-WAN', 'Network Virtualization'],
                'certifications': ['Cisco Certified DevNet Associate', 'VMware Certified Professional – Network Virtualization']
            },
            'Frontend Engineer': {
                'programming_languages': ['JavaScript', 'TypeScript', 'HTML', 'CSS'],
                'frameworks': ['React', 'Angular', 'Vue.js', 'Next.js', 'Svelte'],
                'tools': ['Webpack', 'Vite', 'Npm', 'Yarn', 'Figma', 'Jest', 'Cypress'],
                'concepts': ['UI/UX', 'Responsive Design', 'Accessibility', 'State Management', 'Web Performance'],
                'certifications': ['Meta Front-End Developer Professional Certificate']
            },
            'Backend Engineer': {
                'programming_languages': ['Python', 'Java', 'Go', 'Node.js', 'SQL', 'C#'],
                'frameworks': ['Django', 'FastAPI', 'Spring Boot', 'Express.js', 'ASP.NET'],
                'databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch'],
                'tools': ['Docker', 'Kubernetes', 'AWS', 'Postman', 'Swagger'],
                'concepts': ['API Design', 'Microservices', 'System Architecture', 'Security', 'Database Optimization'],
                'certifications': ['Google Professional Cloud Developer']
            },
            'Fullstack Developer': {
                'programming_languages': ['JavaScript', 'TypeScript', 'Python', 'SQL'],
                'frameworks': ['React', 'Node.js', 'Express.js', 'Django', 'Next.js'],
                'databases': ['PostgreSQL', 'MongoDB', 'MySQL'],
                'tools': ['Git', 'Docker', 'AWS', 'Jenkins'],
                'concepts': ['Full Stack Development', 'RESTful APIs', 'CI/CD', 'Authorization/Authentication', 'DevOps'],
                'certifications': ['Full Stack Web Development Professional Certificate']
            }
        }
        
        # Setup Patterns for Matcher
        if self.matcher:
            self._setup_patterns()

    def _setup_patterns(self):
        """Build spaCy patterns for all multi-word skills in job_skills."""
        if not self.matcher:
            return
            
        seen_patterns = set()
        
        # Automatically find all multi-word skills from predefined sets
        for role_data in self.job_skills.values():
            for category_skills in role_data.values():
                for skill in category_skills:
                    if ' ' in skill:
                        skill_lower = skill.lower()
                        if skill_lower not in seen_patterns:
                            # Create a spaCy pattern: each word as a separate token
                            words = skill_lower.split()
                            pattern = [{"LOWER": word} for word in words]
                            self.matcher.add(skill_lower.upper().replace(' ', '_'), [pattern])
                            seen_patterns.add(skill_lower)
                            
        # Adding common manual patterns if needed
        self.matcher.add("WEB_PERFORMANCE", [[{"LOWER": "web"}, {"LOWER": "performance"}]])

    def get_available_roles(self):
        return sorted(list(self.job_skills.keys()))

    def extract_skills(self, text):
        """Extract skills using High-Precision Hybrid approach."""
        found_skills = set()
        text_clean = re.sub(r'[^\w\s#+.-]', ' ', text) # Keep C++, C#, .NET
        text_lower = text_clean.lower()
        
        # 1. spaCy Matcher (for multi-word skills) - Highest Precision
        if self.nlp:
            doc = self.nlp(text_lower)
            matches = self.matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                found_skills.add(span.text.lower())
                
        # 2. Refined Keyword Matching (Single Word & Precision Check)
        # Collect all potential skills to check
        all_potential_skills = set()
        for role in self.job_skills.values():
            for category in role.values():
                all_potential_skills.update([s.lower() for s in category])
        
        for skill in all_potential_skills:
            if skill in found_skills: continue # Already found by Matcher
            
            # Stricter boundary check for precision
            # Avoids "Java" matching in "Javascript" or "AI" matching in "Main"
            pattern = rf'(?i)\b{re.escape(skill)}\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
                
        return found_skills

    def analyze(self, text, job_role):
        """Production analysis with detailed breakdown."""
        if job_role not in self.job_skills:
            return {'error': 'Job role not supported'}

        found_skills = self.extract_skills(text)
        required_role_skills = self.job_skills[job_role]
        
        results = {
            'job_role': job_role,
            'match_percentage': 0,
            'matched_skills': [],
            'missing_skills': [],
            'matched_by_category': {},
            'missing_by_category': {},
            'analysis_summary': {}
        }
        
        total_required = 0
        total_matched = 0
        
        for category, skills in required_role_skills.items():
            cat_required = [s.lower() for s in skills]
            cat_matched = [s for s in cat_required if s in found_skills]
            cat_missing = [s for s in cat_required if s not in found_skills]
            
            total_required += len(cat_required)
            total_matched += len(cat_matched)
            
            if cat_matched:
                results['matched_by_category'][category] = cat_matched
                results['matched_skills'].extend(cat_matched)
            if cat_missing:
                results['missing_by_category'][category] = cat_missing
                results['missing_skills'].extend(cat_missing)

        # Calculate rule-based match percentage
        if total_required > 0:
            results['match_percentage'] = int((total_matched / total_required) * 100)
        else:
            results['match_percentage'] = 0

        # Advanced AI Analysis (Gemini)
        ai_analysis = None
        if self.ai_service:
            ai_analysis = self.ai_service.analyze_resume(text, job_role)
            
        if ai_analysis and isinstance(ai_analysis, dict):
            results['readiness_score'] = ai_analysis.get('readiness_score', results['match_percentage'])
            results['ai_insights'] = {
                'semantic_summary': ai_analysis.get('semantic_match_summary'),
                'curated_recommendations': ai_analysis.get('curated_recommendations', []),
                'best_fit_role': ai_analysis.get('best_fit_role'),
                'best_fit_reason': ai_analysis.get('best_fit_reason')
            }
        else:
            results['readiness_score'] = results['match_percentage']
            results['ai_insights'] = {
                'semantic_summary': "Advanced AI analysis is currently unavailable.",
                'curated_recommendations': ["Please ensure your API key is valid.", "Try again in a few moments."],
                'best_fit_role': None,
                'best_fit_reason': None
            }

        # Generate Summary (using readiness score if available)
        results['analysis_summary'] = self._generate_summary(results.get('readiness_score', results['match_percentage']))
        
        return results

    def _generate_summary(self, score):
        if score >= 80: return {'rating': 'Excellent', 'message': 'Perfect fit! Your skills align strongly with this role.'}
        if score >= 60: return {'rating': 'Good', 'message': 'Solid match. You have most core competencies but can improve.'}
        if score >= 40: return {'rating': 'Fair', 'message': 'Some overlap found. Targeted learning is recommended.'}
        return {'rating': 'Developing', 'message': 'Build foundational skills in the missing categories to become competitive.'}
