#!/usr/bin/env python3
"""
Demo script for Skill-Bridge Career Navigator
Demonstrates the core functionality without running the web server
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import SkillGapAnalyzer

def run_demo():
    """Run a demonstration of the skill gap analyzer"""
    print("=" * 60)
    print("SKILL-BRIDGE CAREER NAVIGATOR - DEMO")
    print("=" * 60)
    
    analyzer = SkillGapAnalyzer()
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Recent Graduate",
            "resume": "I am a recent computer science graduate with experience in Python, JavaScript, and basic web development. I built a portfolio website and contributed to open source projects.",
            "target_role": "Software Engineer"
        },
        {
            "name": "Career Switcher", 
            "resume": "I have 3 years of experience as a business analyst with strong SQL skills and Python for data analysis. I want to transition to a more technical role.",
            "target_role": "Data Scientist"
        },
        {
            "name": "Frontend Developer",
            "resume": "Experienced frontend developer with expertise in JavaScript, React, HTML, CSS, and TypeScript. I've built multiple responsive web applications.",
            "target_role": "Full Stack Developer"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i} {'='*20}")
        print(f"User: {scenario['name']}")
        print(f"Target Role: {scenario['target_role']}")
        print(f"Resume: {scenario['resume'][:100]}...")
        
        # Extract skills
        user_skills = analyzer.extract_skills(scenario['resume'])
        print(f"\n📋 Extracted Skills: {', '.join(user_skills)}")
        
        # Analyze skill gaps
        gap_analysis = analyzer.analyze_skill_gap(user_skills, scenario['target_role'])
        
        if 'error' in gap_analysis:
            print(f"❌ Error: {gap_analysis['error']}")
            continue
            
        print(f"\n📊 Gap Analysis Results:")
        print(f"   Jobs Analyzed: {gap_analysis['total_jobs_analyzed']}")
        print(f"   Missing Skills: {len(gap_analysis['missing_skills'])}")
        
        if gap_analysis['missing_skills']:
            print("   Top Missing Skills:")
            for skill in gap_analysis['missing_skills'][:3]:
                print(f"     • {skill['skill']} ({skill['priority']} priority - found in {skill['frequency']} jobs)")
        
        # Generate learning roadmap
        roadmap = analyzer.generate_learning_roadmap(gap_analysis['missing_skills'])
        if roadmap:
            print(f"\n🎯 Learning Roadmap ({len(roadmap)} skills to learn):")
            for item in roadmap[:2]:  # Show top 2
                print(f"   • {item['skill']} ({item['estimated_time']})")
                for resource in item['resources'][:1]:  # Show top resource
                    print(f"     - {resource['name']} ({resource['type']})")
        
        # Generate interview questions
        questions = analyzer.generate_interview_questions(user_skills, scenario['target_role'])
        print(f"\n🎤 Interview Questions ({len(questions)} questions):")
        for i, question in enumerate(questions[:3], 1):
            print(f"   {i}. {question}")
        
        print("\n" + "-"*60)
    
    print(f"\n{'='*60}")
    print("DEMO COMPLETE! 🎉")
    print("To run the web application: python app.py")
    print("To run tests: pytest tests/")
    print(f"{'='*60}")

if __name__ == '__main__':
    run_demo()
