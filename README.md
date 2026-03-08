# Skill-Bridge Career Navigator

Ever stare at job descriptions and feel like there's this massive gap between what you learned in class and what employers actually want? Yeah, me too. So I built an AI-powered tool that helps figure out exactly what skills you're missing and how to get them.

Basically, you paste your resume, pick your dream job, and the app tells you:
- What skills you already have vs. what you need
- Exactly which courses to take to fill those gaps
- Interview questions you'll probably face

## What It Actually Does

- **Gap Analysis**: Compares your skills against real job postings to show exactly what you're missing
- **Learning Roadmap**: Gives you specific courses (free and paid) to fill those gaps, with time estimates
- **Interview Questions**: Generates practice questions based on your skills and target role
- **Clean Interface**: Actually looks good and works on your phone
- **AI Magic**: Uses NLP to parse your resume and figure out what you know

## About Me
**Name:** Jayda-Louise Nkansah  
**Project:** Skill-Bridge Career Navigator  
**Time Spent:** About 5 hours
**Demo Video:** https://youtu.be/ZrEPpg5Yaj4

## Quick Start:

### Prerequisites:
- Python 3.8 or higher
- pip package manager

### Run Commands:
```bash
# Clone the repository
git clone https://github.com/jnkansah/ai-career-skill-gap-analyzer.git
cd ai-career-skill-gap-analyzer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5001`

**Note**: If port 5001 is in use, you can change the port in `app.py` (line 334).

### Test Commands:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app

# Run specific test file
pytest tests/test_analyzer.py
```

## AI Stuff

### Did I use AI helpers? (Yes/No)
Yes. I used ChatGPT throughout this project for debugging help as well as explanations when stuck. It helped with the frontend design as well, especially with the CSS and HTML structure.

### How I made sure the AI suggestions actually worked:
- Tested everything manually through the web interface
- Ran comprehensive unit and integration tests (28 tests passing)
- Verified AI outputs against expected results for sample inputs

### One AI suggestion I rejected:
The AI initially suggested using complex transformer models for skill extraction. I said no and went with a simpler keyword-based approach because:
1. It's way more transparent because you can actually see why it thinks you know "Python"
2. Much faster for real-time use 
3. Easier to debug when things go wrong

## Tradeoffs & Prioritization:

### What did you cut to stay within the 4–6 hour limit?
- Advanced NLP with spaCy for more sophisticated skill extraction
- Real-time job scraping from LinkedIn/Indeed
- User authentication and profile persistence
- Advanced visualizations and charts
- Email notifications for learning reminders
- Integration with actual learning platform APIs

### What I'd build next if I had more time:
1. **Real Job Data Integration**: Connect to actual job posting APIs for live market analysis
2. **User Profiles**: Add user accounts to save progress and track learning journeys
3. **Mobile App**: Create a React Native mobile version

### Known limitations:
- **Interview Questions**: Currently uses a predefined question bank. Ideally, the AI would generate unique questions based on your profile and target role, but that would require much more sophisticated NLP models.
- **Sample Data**: Using synthetic job descriptions and resumes I created. Real job market data would be way more complex and nuanced.
- **Skill Extraction**: Relies on keyword matching, so it might miss context-specific skills or industry jargon.
- **Static Learning Resources**: Courses don't update in real-time with new offerings or changing industry demands.
- **Limited Job Roles**: Only covers the roles I included in the dataset, no way to add custom roles yet.

## Technical Architecture

### Tech Stack:
- **Backend**: Flask (Python)
- **Frontend**: HTML5, JavaScript, CSS
- **Data Processing**: Pandas, NumPy, scikit-learn
- **NLP**: NLTK for text preprocessing
- **Testing**: Pytest

### Key Components:
1. **SkillGapAnalyzer**: Core analysis engine
2. **Web Interface**: Responsive frontend with real-time updates
3. **Data Layer**: CSV/JSON datasets for jobs and sample resumes
4. **API Endpoints**: RESTful API for analysis services

### Test Results:
- 95%+ code coverage for core functionality
- All critical paths tested
- Performance benchmarks included

## License

MIT License - feel free to use this project for educational or commercial purposes.