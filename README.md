# AI Based Resume Skill Gap Detection System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

An intelligent web application that analyzes resumes and identifies skill gaps for target job roles using NLP and keyword matching techniques.

## 🌟 Features

- **Smart Resume Upload**: Support for PDF, DOCX, and TXT file formats
- **Alternative Text Input**: Paste resume text directly for quick analysis
- **Multiple Job Roles**: Pre-configured analysis for 8+ professional roles
- **AI-Powered Analysis**: Uses spaCy NLP for intelligent skill extraction
- **Skill Gap Detection**: Identifies matched and missing skills
- **Interactive Dashboard**: Beautiful, responsive UI with real-time results
- **Match Percentage**: Calculate how well your resume matches job requirements
- **Categorized Results**: Skills organized by category for better insights

## 📋 Supported Job Roles

- Software Engineer
- Data Analyst
- Data Scientist
- Web Developer
- DevOps Engineer
- Mobile Developer
- UI/UX Designer
- Product Manager

## 🛠️ Tech Stack

**Frontend:**
- HTML5
- CSS3 (Modern design with gradients and animations)
- Vanilla JavaScript (ES6+)

**Backend:**
- Python 3.8+
- Flask 3.0.0
- spaCy (NLP processing)
- PyPDF2 (PDF text extraction)
- python-docx (DOCX text extraction)

## 📁 Project Structure

```
AI Based Resume Skill Gap Detection System/
│
├── app.py                      # Main Flask application
├── skill_analyzer.py           # Skill extraction and analysis logic
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore file
│
├── static/                     # Frontend files
│   ├── index.html             # Main HTML page
│   ├── styles.css             # CSS styling
│   └── script.js              # Frontend JavaScript
│
└── uploads/                    # Temporary upload folder (auto-created)
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd "AI Based Resume Skill Gap Detection System"
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 💡 How to Use

1. **Select Job Role**: Choose your target job role from the dropdown menu
2. **Upload Resume**: Either upload a PDF/DOCX file or paste your resume text
3. **Analyze**: Click the "Analyze Resume" button
4. **View Results**: See your skill match percentage, matched skills, and skill gaps
5. **Improve**: Use the missing skills list to guide your learning path

## 🎨 Features Showcase

### Skill Extraction
The system uses advanced NLP techniques to extract skills from your resume, including:
- Programming languages
- Frameworks and libraries
- Tools and technologies
- Databases
- Soft skills and concepts

### Intelligent Matching
- Compares extracted skills with role-specific requirements
- Calculates match percentage
- Categorizes skills by type (frontend, backend, tools, etc.)
- Provides actionable insights

### User Experience
- Clean, modern UI with gradient themes
- Responsive design for all devices
- Smooth animations and transitions
- Real-time feedback and loading states
- Tab-based input options

## 🔧 Configuration

### Adding New Job Roles

Edit `skill_analyzer.py` and add your custom job role to the `job_skills` dictionary:

```python
'Your Job Role': {
    'category_name': ['Skill1', 'Skill2', 'Skill3'],
    'another_category': ['SkillA', 'SkillB'],
    # Add more categories as needed
}
```

### Customizing Skills

Modify the skill lists in `skill_analyzer.py` to match your specific requirements for each job role.

## 🐛 Troubleshooting

### spaCy Model Not Found
If you see a warning about the spaCy model, run:
```bash
python -m spacy download en_core_web_sm
```

### Port Already in Use
If port 5000 is busy, edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### File Upload Issues
- Ensure uploaded files are under 16MB
- Only PDF, DOCX, and TXT formats are supported
- Check file permissions in the project directory

## 📊 API Endpoints

### GET `/api/job-roles`
Returns list of available job roles
```json
{
  "roles": ["Software Engineer", "Data Analyst", ...]
}
```

### POST `/api/analyze`
Analyzes resume and returns skill gap data

**Parameters:**
- `job_role`: Selected job role (required)
- `resume_file`: Resume file (PDF/DOCX/TXT) OR
- `resume_text`: Resume text content

**Response:**
```json
{
  "job_role": "Software Engineer",
  "match_percentage": 75.5,
  "matched_skills": [...],
  "missing_skills": [...],
  "matched_by_category": {...},
  "missing_by_category": {...},
  "analysis_summary": {...}
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more job roles
- Improve skill extraction algorithms
- Enhance the UI/UX
- Fix bugs and issues
- Add new features

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ for helping job seekers identify and bridge skill gaps.

## 🙏 Acknowledgments

- spaCy for NLP capabilities
- Flask for the web framework
- The open-source community

## 📞 Support

For issues, questions, or suggestions, please open an issue in the project repository.

---

**Happy Job Hunting! 🎯**
