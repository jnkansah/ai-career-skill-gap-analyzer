import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
import json

class TestFlaskApp:
    
    def setup_method(self):
        """Setup test environment"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_index_route(self):
        """Test index route returns HTML"""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'Skill-Bridge Career Navigator' in response.data
        assert b'html' in response.data.lower()
    
    def test_analyze_route_valid_input(self):
        """Test analyze route with valid input"""
        test_data = {
            'resume': 'I have experience with Python and JavaScript',
            'targetRole': 'Software Engineer'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'gap_analysis' in data
        assert 'learning_roadmap' in data
        assert 'interview_questions' in data
    
    def test_analyze_route_missing_resume(self):
        """Test analyze route with missing resume"""
        test_data = {
            'targetRole': 'Software Engineer'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        # Should handle gracefully (validation happens in frontend)
        assert response.status_code == 200
    
    def test_analyze_route_missing_role(self):
        """Test analyze route with missing target role"""
        test_data = {
            'resume': 'I have experience with Python and JavaScript'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
    
    def test_analyze_route_invalid_role(self):
        """Test analyze route with invalid target role"""
        test_data = {
            'resume': 'I have experience with Python and JavaScript',
            'targetRole': 'Invalid Role That Does Not Exist'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_analyze_route_empty_input(self):
        """Test analyze route with empty input"""
        test_data = {
            'resume': '',
            'targetRole': ''
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
    
    def test_analyze_route_complex_resume(self):
        """Test analyze route with complex resume text"""
        test_data = {
            'resume': '''
            John Doe
            Software Developer with 3 years of experience
            
            Skills:
            - Python (Django, Flask)
            - JavaScript (React, Node.js)
            - SQL (PostgreSQL, MySQL)
            - AWS (EC2, S3)
            - Docker
            - Git
            
            Experience:
            - Built web applications using React and Python
            - Deployed applications to AWS
            - Worked with SQL databases
            - Used Docker for containerization
            ''',
            'targetRole': 'Full Stack Developer'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'gap_analysis' in data
        assert 'learning_roadmap' in data
        assert 'interview_questions' in data
        
        # Check that skills were extracted
        gap_analysis = data['gap_analysis']
        assert len(gap_analysis['user_skills']) >= 3
    
    def test_roles_endpoint(self):
        """Test roles endpoint"""
        response = self.client.get('/api/roles')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
        assert 'Software Engineer' in data
        assert 'Data Scientist' in data
    
    def test_analyze_route_response_structure(self):
        """Test that analyze route returns correct structure"""
        test_data = {
            'resume': 'Python, JavaScript, React, SQL experience',
            'targetRole': 'Software Engineer'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check top-level structure
        assert 'gap_analysis' in data
        assert 'learning_roadmap' in data
        assert 'interview_questions' in data
        
        # Check gap_analysis structure
        gap_analysis = data['gap_analysis']
        assert 'role' in gap_analysis
        assert 'user_skills' in gap_analysis
        assert 'missing_skills' in gap_analysis
        assert 'total_jobs_analyzed' in gap_analysis
        
        # Check learning_roadmap structure
        roadmap = data['learning_roadmap']
        assert isinstance(roadmap, list)
        if roadmap:  # If not empty
            assert 'skill' in roadmap[0]
            assert 'priority' in roadmap[0]
            assert 'resources' in roadmap[0]
            assert 'estimated_time' in roadmap[0]
        
        # Check interview_questions structure
        questions = data['interview_questions']
        assert isinstance(questions, list)
        assert all(isinstance(q, str) for q in questions)

class TestFlaskAppErrorHandling:
    """Test error handling and edge cases"""
    
    def setup_method(self):
        """Setup test environment"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_invalid_json_input(self):
        """Test handling of invalid JSON input"""
        response = self.client.post('/analyze',
                                   data='invalid json',
                                   content_type='application/json')
        
        # Should handle gracefully
        assert response.status_code == 400
    
    def test_missing_content_type(self):
        """Test handling of missing content type"""
        response = self.client.post('/analyze',
                                   data=json.dumps({
                                       'resume': 'test',
                                       'targetRole': 'test'
                                   }))
        
        # Should handle gracefully (Flask returns 415 for unsupported media type)
        assert response.status_code in [400, 415]
    
    def test_very_long_resume(self):
        """Test handling of very long resume text"""
        long_resume = 'Python ' * 1000  # Create a very long string
        
        test_data = {
            'resume': long_resume,
            'targetRole': 'Software Engineer'
        }
        
        response = self.client.post('/analyze',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
        
        assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__])
