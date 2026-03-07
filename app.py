from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import json
import os

app = Flask(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class SkillGapAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.jobs_data = None
        self.learning_resources = self.load_learning_resources()
        
    def load_learning_resources(self):
        """Load predefined learning resources for different skills"""
        return {
            'python': [
                {'name': 'Python for Everybody', 'provider': 'Coursera', 'duration': '3 months', 'type': 'free', 'url': '#'},
                {'name': 'Complete Python Bootcamp', 'provider': 'Udemy', 'duration': '2 months', 'type': 'paid', 'url': '#'}
            ],
            'javascript': [
                {'name': 'JavaScript Algorithms and Data Structures', 'provider': 'freeCodeCamp', 'duration': '1 month', 'type': 'free', 'url': '#'},
                {'name': 'Modern JavaScript Tutorial', 'provider': 'JavaScript.info', 'duration': '2 months', 'type': 'free', 'url': '#'}
            ],
            'react': [
                {'name': 'React - The Complete Guide', 'provider': 'Udemy', 'duration': '1 month', 'type': 'paid', 'url': '#'},
                {'name': 'React Tutorial', 'provider': 'React Documentation', 'duration': '2 weeks', 'type': 'free', 'url': '#'}
            ],
            'aws': [
                {'name': 'AWS Cloud Practitioner', 'provider': 'AWS Training', 'duration': '1 month', 'type': 'free', 'url': '#'},
                {'name': 'AWS Solutions Architect', 'provider': 'Udemy', 'duration': '2 months', 'type': 'paid', 'url': '#'}
            ],
            'docker': [
                {'name': 'Docker Mastery', 'provider': 'Udemy', 'duration': '1 week', 'type': 'paid', 'url': '#'},
                {'name': 'Docker Documentation', 'provider': 'Docker', 'duration': '2 weeks', 'type': 'free', 'url': '#'}
            ],
            'sql': [
                {'name': 'SQL for Data Analysis', 'provider': 'Coursera', 'duration': '1 month', 'type': 'free', 'url': '#'},
                {'name': 'Complete SQL Bootcamp', 'provider': 'Udemy', 'duration': '2 months', 'type': 'paid', 'url': '#'}
            ],
            'machine learning': [
                {'name': 'Machine Learning A-Z', 'provider': 'Udemy', 'duration': '3 months', 'type': 'paid', 'url': '#'},
                {'name': 'Introduction to Machine Learning', 'provider': 'Coursera', 'duration': '2 months', 'type': 'free', 'url': '#'}
            ],
            'git': [
                {'name': 'Git & GitHub Crash Course', 'provider': 'freeCodeCamp', 'duration': '1 week', 'type': 'free', 'url': '#'},
                {'name': 'Pro Git Book', 'provider': 'Git Documentation', 'duration': '2 weeks', 'type': 'free', 'url': '#'}
            ]
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def extract_skills(self, text):
        """Extract skills from text using keyword matching"""
        tech_skills = [
            'python', 'javascript', 'java', 'react', 'nodejs', 'html', 'css', 'sql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'mongodb', 'postgresql',
            'machine learning', 'data analysis', 'tensorflow', 'pytorch', 'flask', 'django',
            'typescript', 'vue', 'angular', 'linux', 'ci/cd', 'testing', 'agile', 'scrum'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        # Check for skills in order of specificity (longer terms first)
        # Handle special cases like javascript vs java
        for skill in sorted(tech_skills, key=len, reverse=True):
            if skill == 'javascript':
                # Only match javascript if the whole word is present
                if re.search(r'\bjavascript\b', text_lower) and skill not in found_skills:
                    found_skills.append(skill)
            elif skill == 'java':
                # Only match java if javascript is not already found
                if re.search(r'\bjava\b', text_lower) and 'javascript' not in found_skills and skill not in found_skills:
                    found_skills.append(skill)
            else:
                # For other skills, check if the whole phrase is present
                if ' ' in skill:
                    # Multi-word skill
                    if skill in text_lower and skill not in found_skills:
                        found_skills.append(skill)
                else:
                    # Single word skill
                    if re.search(r'\b' + re.escape(skill) + r'\b', text_lower) and skill not in found_skills:
                        found_skills.append(skill)
        
        return found_skills
    
    def load_job_data(self):
        """Load synthetic job data"""
        if self.jobs_data is None:
            try:
                self.jobs_data = pd.read_csv('data/job_descriptions.csv')
                # Convert pipe-separated skills to lists
                self.jobs_data['required_skills'] = self.jobs_data['required_skills'].str.split('|')
            except FileNotFoundError:
                # Create sample data if file doesn't exist
                self.jobs_data = self.create_sample_job_data()
        return self.jobs_data
    
    def create_sample_job_data(self):
        """Create sample job descriptions"""
        jobs = [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'description': 'We are looking for a Software Engineer with experience in Python, JavaScript, React, and SQL. Knowledge of AWS and Docker is a plus.',
                'required_skills': ['python', 'javascript', 'react', 'sql', 'aws', 'docker'],
                'experience_level': 'Mid-level'
            },
            {
                'title': 'Data Scientist',
                'company': 'Data Analytics Inc',
                'description': 'Seeking a Data Scientist with strong Python skills, machine learning experience, and SQL knowledge. TensorFlow/PyTorch experience required.',
                'required_skills': ['python', 'machine learning', 'sql', 'tensorflow', 'data analysis'],
                'experience_level': 'Senior'
            },
            {
                'title': 'Frontend Developer',
                'company': 'Web Solutions',
                'description': 'Frontend Developer needed with expertise in JavaScript, React, HTML/CSS, and TypeScript. Experience with Git and modern build tools required.',
                'required_skills': ['javascript', 'react', 'html', 'css', 'typescript', 'git'],
                'experience_level': 'Mid-level'
            },
            {
                'title': 'Cloud Engineer',
                'company': 'Cloud Systems',
                'description': 'Cloud Engineer with AWS experience, Docker, Kubernetes, and Linux. Knowledge of CI/CD pipelines and infrastructure as code.',
                'required_skills': ['aws', 'docker', 'kubernetes', 'linux', 'ci/cd'],
                'experience_level': 'Senior'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'description': 'Full Stack Developer with Python/Node.js backend, React frontend, PostgreSQL, and AWS deployment experience.',
                'required_skills': ['python', 'javascript', 'react', 'postgresql', 'aws', 'nodejs'],
                'experience_level': 'Mid-level'
            }
        ]
        return pd.DataFrame(jobs)
    
    def analyze_skill_gap(self, user_skills, target_role):
        """Analyze skill gaps between user skills and job requirements"""
        jobs = self.load_job_data()
        role_jobs = jobs[jobs['title'].str.contains(target_role, case=False, na=False)]
        
        if len(role_jobs) == 0:
            return {'error': f'No jobs found for role: {target_role}'}
        
        # Get all required skills for this role
        all_required_skills = []
        for skills in role_jobs['required_skills']:
            all_required_skills.extend(skills)
        
        # Count skill frequency
        skill_frequency = {}
        for skill in all_required_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        # Find missing skills
        user_skills_lower = [skill.lower() for skill in user_skills]
        missing_skills = []
        
        for skill in skill_frequency:
            if skill not in user_skills_lower:
                missing_skills.append({
                    'skill': skill,
                    'frequency': skill_frequency[skill],
                    'priority': 'High' if skill_frequency[skill] >= 3 else 'Medium'
                })
        
        # Sort by frequency
        missing_skills.sort(key=lambda x: x['frequency'], reverse=True)
        
        return {
            'role': target_role,
            'user_skills': user_skills,
            'missing_skills': missing_skills,
            'total_jobs_analyzed': len(role_jobs)
        }
    
    def generate_learning_roadmap(self, missing_skills):
        """Generate learning roadmap based on missing skills"""
        roadmap = []
        
        for skill_info in missing_skills:
            skill = skill_info['skill']
            if skill in self.learning_resources:
                resources = self.learning_resources[skill]
                roadmap.append({
                    'skill': skill,
                    'priority': skill_info['priority'],
                    'resources': resources[:2],  # Top 2 resources
                    'estimated_time': self.estimate_learning_time(skill)
                })
        
        return roadmap
    
    def estimate_learning_time(self, skill):
        """Estimate learning time for a skill"""
        time_mapping = {
            'python': '2-3 months',
            'javascript': '1-2 months',
            'react': '1-2 months',
            'aws': '2-3 months',
            'docker': '2-4 weeks',
            'sql': '1-2 months',
            'machine learning': '3-6 months',
            'git': '1-2 weeks'
        }
        return time_mapping.get(skill, '1-2 months')
    
    def generate_interview_questions(self, user_skills, target_role):
        """Generate mock interview questions based on skills and role"""
        question_bank = {
            'python': [
                'Explain the difference between list and tuple in Python',
                'How does Python handle memory management?',
                'What are Python decorators and how do they work?'
            ],
            'javascript': [
                'Explain event bubbling and event capturing',
                'What is the difference between let, const, and var?',
                'How does prototypal inheritance work in JavaScript?'
            ],
            'react': [
                'Explain the React component lifecycle',
                'What is the difference between controlled and uncontrolled components?',
                'How does React Virtual DOM work?'
            ],
            'sql': [
                'What is the difference between INNER JOIN and LEFT JOIN?',
                'Explain database normalization',
                'How do you optimize SQL queries?'
            ],
            'aws': [
                'What is the difference between EC2 and Lambda?',
                'Explain VPC and its components',
                'How do you secure AWS resources?'
            ]
        }
        
        questions = []
        for skill in user_skills:
            if skill in question_bank:
                questions.extend(question_bank[skill][:2])  # 2 questions per skill
        
        # Add role-specific questions
        role_questions = {
            'software engineer': [
                'How do you approach debugging a complex issue?',
                'Describe your experience with version control systems'
            ],
            'data scientist': [
                'How do you handle imbalanced datasets?',
                'Explain the bias-variance tradeoff'
            ],
            'frontend developer': [
                'How do you ensure cross-browser compatibility?',
                'What are your thoughts on responsive design?'
            ]
        }
        
        if target_role.lower() in role_questions:
            questions.extend(role_questions[target_role.lower()])
        
        return questions[:8]  # Return max 8 questions

# Initialize analyzer
analyzer = SkillGapAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    user_resume = data.get('resume', '')
    target_role = data.get('targetRole', '')
    
    # Extract skills from resume
    user_skills = analyzer.extract_skills(user_resume)
    
    # Analyze skill gaps
    gap_analysis = analyzer.analyze_skill_gap(user_skills, target_role)
    
    if 'error' in gap_analysis:
        return jsonify(gap_analysis)
    
    # Generate learning roadmap
    roadmap = analyzer.generate_learning_roadmap(gap_analysis['missing_skills'])
    
    # Generate interview questions
    interview_questions = analyzer.generate_interview_questions(user_skills, target_role)
    
    return jsonify({
        'gap_analysis': gap_analysis,
        'learning_roadmap': roadmap,
        'interview_questions': interview_questions
    })

@app.route('/api/roles')
def get_roles():
    """Get available job roles"""
    jobs = analyzer.load_job_data()
    roles = jobs['title'].unique().tolist()
    return jsonify(roles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
