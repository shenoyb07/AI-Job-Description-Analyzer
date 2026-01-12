def extract_skills(text):
    """
    Extracts technical and soft skills from text using keyword matching.
    """
    technical_skills_keywords = {
        "python", "java", "sql", "machine learning", "cloud", "nlp", "data analysis", 
        "javascript", "react", "node.js", "docker", "kubernetes", "aws", "azure", 
        "gcp", "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", 
        "c++", "c#", "ruby", "go", "rust", "r", "swift", "kotlin", "tableau", "power bi"
    }
    
    soft_skills_keywords = {
        "communication", "teamwork", "leadership", "problem solving", "collaboration",
        "interpersonal", "adaptability", "critical thinking", "time management",
        "creativity", "emotional intelligence", "conflict resolution"
    }

    text_lower = text.lower()
    
    extracted_tech = [skill for skill in technical_skills_keywords if skill in text_lower]
    extracted_soft = [skill for skill in soft_skills_keywords if skill in text_lower]

    return {
        "technical_skills": extracted_tech,
        "soft_skills": extracted_soft
    }
