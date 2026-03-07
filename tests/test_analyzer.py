import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import SkillGapAnalyzer

class TestSkillGapAnalyzer:
    
    def setup_method(self):
        """Setup test environment"""
        self.analyzer = SkillGapAnalyzer()
    
    def test_extract_skills_basic(self):
        """Test basic skill extraction"""
        text = "I have experience with Python, JavaScript, and React development"
        skills = self.analyzer.extract_skills(text)
        
        assert 'python' in skills
        assert 'javascript' in skills
        assert 'react' in skills
        assert len(skills) == 3
    
    def test_extract_skills_case_insensitive(self):
        """Test skill extraction is case insensitive"""
        text = "PYTHON JavaSCRIPT REACT"
        skills = self.analyzer.extract_skills(text)
        
        assert 'python' in skills
        assert 'javascript' in skills
        assert 'react' in skills
    
    def test_extract_skills_no_match(self):
        """Test skill extraction with no matches"""
        text = "I have experience with management and communication"
        skills = self.analyzer.extract_skills(text)
        
        assert len(skills) == 0
    
    def test_preprocess_text(self):
        """Test text preprocessing"""
        text = "Hello World! This is a TEST."
        processed = self.analyzer.preprocess_text(text)
        
        assert 'hello' in processed
        assert 'world' in processed
        assert 'test' in processed
        assert '!' not in processed
        assert 'this' not in processed  # Should be removed as stop word
    
    def test_analyze_skill_gap_valid_role(self):
        """Test skill gap analysis for valid role"""
        user_skills = ['python', 'javascript']
        target_role = 'Software Engineer'
        
        result = self.analyzer.analyze_skill_gap(user_skills, target_role)
        
        assert 'role' in result
        assert 'user_skills' in result
        assert 'missing_skills' in result
        assert 'total_jobs_analyzed' in result
        assert result['role'] == target_role
        assert result['user_skills'] == user_skills
        assert len(result['missing_skills']) > 0
    
    def test_analyze_skill_gap_invalid_role(self):
        """Test skill gap analysis for invalid role"""
        user_skills = ['python', 'javascript']
        target_role = 'Invalid Role'
        
        result = self.analyzer.analyze_skill_gap(user_skills, target_role)
        
        assert 'error' in result
    
    def test_generate_learning_roadmap(self):
        """Test learning roadmap generation"""
        missing_skills = [
            {'skill': 'python', 'priority': 'High'},
            {'skill': 'react', 'priority': 'Medium'}
        ]
        
        roadmap = self.analyzer.generate_learning_roadmap(missing_skills)
        
        assert len(roadmap) == 2
        assert all('skill' in item for item in roadmap)
        assert all('priority' in item for item in roadmap)
        assert all('resources' in item for item in roadmap)
        assert all('estimated_time' in item for item in roadmap)
    
    def test_generate_learning_roadmap_empty(self):
        """Test learning roadmap with empty skills"""
        roadmap = self.analyzer.generate_learning_roadmap([])
        assert len(roadmap) == 0
    
    def test_generate_interview_questions(self):
        """Test interview question generation"""
        user_skills = ['python', 'javascript']
        target_role = 'Software Engineer'
        
        questions = self.analyzer.generate_interview_questions(user_skills, target_role)
        
        assert len(questions) > 0
        assert all(isinstance(q, str) for q in questions)
        assert len(questions) <= 8  # Should return max 8 questions
    
    def test_generate_interview_questions_no_skills(self):
        """Test interview question generation with no skills"""
        user_skills = []
        target_role = 'Software Engineer'
        
        questions = self.analyzer.generate_interview_questions(user_skills, target_role)
        
        # Should still return role-specific questions
        assert len(questions) > 0
    
    def test_estimate_learning_time(self):
        """Test learning time estimation"""
        time_python = self.analyzer.estimate_learning_time('python')
        time_unknown = self.analyzer.estimate_learning_time('unknown_skill')
        
        assert time_python == '2-3 months'
        assert time_unknown == '1-2 months'  # Default time
    
    def test_load_job_data(self):
        """Test loading job data"""
        jobs = self.analyzer.load_job_data()
        
        assert isinstance(jobs, object)  # pandas DataFrame
        assert len(jobs) > 0
        assert 'title' in jobs.columns
        assert 'required_skills' in jobs.columns
    
    def test_create_sample_job_data(self):
        """Test sample job data creation"""
        jobs = self.analyzer.create_sample_job_data()
        
        assert len(jobs) == 5
        assert all('title' in job for job in jobs.to_dict('records'))
        assert all('required_skills' in job for job in jobs.to_dict('records'))
        assert all('description' in job for job in jobs.to_dict('records'))

class TestSkillGapAnalyzerIntegration:
    """Integration tests for the complete workflow"""
    
    def setup_method(self):
        """Setup test environment"""
        self.analyzer = SkillGapAnalyzer()
    
    def test_complete_workflow(self):
        """Test complete analysis workflow"""
        # Simulate user input
        resume_text = "I have experience with Python and JavaScript. I built web applications using these technologies."
        target_role = "Software Engineer"
        
        # Extract skills
        user_skills = self.analyzer.extract_skills(resume_text)
        
        # Analyze skill gaps
        gap_analysis = self.analyzer.analyze_skill_gap(user_skills, target_role)
        
        # Generate roadmap
        roadmap = self.analyzer.generate_learning_roadmap(gap_analysis['missing_skills'])
        
        # Generate interview questions
        questions = self.analyzer.generate_interview_questions(user_skills, target_role)
        
        # Verify all components work together
        assert len(user_skills) >= 2
        assert 'missing_skills' in gap_analysis
        assert isinstance(roadmap, list)
        assert isinstance(questions, list)
        assert len(questions) > 0
    
    def test_user_with_all_skills(self):
        """Test user who has all required skills"""
        user_skills = ['python', 'javascript', 'react', 'sql', 'aws', 'docker', 'git', 'testing']
        target_role = "Software Engineer"
        
        gap_analysis = self.analyzer.analyze_skill_gap(user_skills, target_role)
        
        # Should have few or no missing skills
        assert len(gap_analysis['missing_skills']) <= 2
    
    def test_user_with_few_skills(self):
        """Test user with minimal skills"""
        user_skills = ['python']
        target_role = "Software Engineer"
        
        gap_analysis = self.analyzer.analyze_skill_gap(user_skills, target_role)
        
        # Should have many missing skills
        assert len(gap_analysis['missing_skills']) >= 3
        
        # Check that missing skills are prioritized
        priorities = [skill['priority'] for skill in gap_analysis['missing_skills']]
        assert 'High' in priorities or 'Medium' in priorities

if __name__ == '__main__':
    pytest.main([__file__])
