# Design Documentation: Skill-Bridge Career Navigator

The Skill-Bridge Career Navigator is basically a smart career coach that looks at what you know, compares it to what employers want, and gives you a concrete plan to get there. No more guessing games - just clear, actionable steps.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Flask App     │    │   Data Layer    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (CSV/JSON)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Analysis      │
                       │   Engine        │
                       └─────────────────┘
```

### Component Architecture

#### 1. Frontend (Web Interface)
- **Technology**: HTML, JavaScript, CSS
- **Responsibility**: User interaction, data visualization, API communication
- **Key Features**:
  - Resume/skills input form
  - Role selection dropdown
  - Results display with animations
  - Responsive design for mobile/desktop

#### 2. Backend (Flask Application)
- **Technology**: Flask, Python
- **Responsibility**: API endpoints, business logic, data processing
- **Key Components**:
  - `/` - Main application page
  - `/analyze` - Skill gap analysis endpoint
  - `/api/roles` - Available job roles endpoint

#### 3. Analysis Engine (SkillGapAnalyzer)
- **Technology**: Python, NLTK, scikit-learn, Pandas
- **Responsibility**: Core analysis algorithms and data processing
- **Key Methods**:
  - `extract_skills()` - Extract skills from text
  - `analyze_skill_gap()` - Compare user skills to job requirements
  - `generate_learning_roadmap()` - Create personalized learning paths
  - `generate_interview_questions()` - Generate role-specific questions

#### 4. Data Layer
- **Technology**: CSV, JSON files
- **Components**:
  - `data/job_descriptions.csv` - Job postings and requirements
  - `data/sample_resumes.json` - Sample user profiles
  - Static learning resources database

## Data Flow

### 1. User Input Flow
```
User Input → Frontend Validation → API Request → Backend Processing → Response → Frontend Display
```

### 2. Analysis Flow
```
Resume Text → Skill Extraction → Gap Analysis → Learning Roadmap → Interview Questions → Results
```

### 3. Data Processing Flow
```
Raw Text → Preprocessing → Tokenization → Skill Matching → Analysis → Recommendations
```

## Core Algorithms

### 1. Skill Extraction Algorithm

**Approach**: Keyword-based extraction with NLP preprocessing

**Steps**:
1. Text preprocessing (lowercase, remove punctuation)
2. Tokenization using NLTK
3. Stop word removal
4. Keyword matching against predefined skill list
5. Skill frequency analysis

**Complexity**: O(n*m) where n = text length, m = skill vocabulary size

### 2. Gap Analysis Algorithm

**Approach**: Set-based comparison with frequency weighting

**Steps**:
1. Filter job descriptions by target role
2. Extract required skills from matching jobs
3. Calculate skill frequency across job postings
4. Identify missing skills (set difference)
5. Prioritize missing skills by frequency

**Formula**:
```
Missing Skills = Required Skills ∩ User Skills
Priority = High if frequency ≥ 3 else Medium
```

### 3. Learning Roadmap Generation

**Approach**: Rule-based mapping with time estimation

**Steps**:
1. Map missing skills to learning resources
2. Estimate completion time per skill
3. Prioritize by skill importance
4. Format as structured roadmap

### 4. Interview Question Generation

**Approach**: Template-based selection with role customization

**Steps**:
1. Select questions based on user skills
2. Add role-specific questions
3. Limit to 8 questions total
4. Format for display