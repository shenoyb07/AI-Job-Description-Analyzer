def detect_experience_level(text):
    """
    Detects experience level (Junior, Mid-level, Senior) from text.
    Uses hierarchical priority: Senior > Mid-level > Junior.
    """
    senior_keywords = ["senior", "lead", "manager", "architect", "principal", "head", "director", "vp"]
    mid_keywords = ["mid-level", "associate", "intermediate", "experienced", "mid"]
    junior_keywords = ["junior", "entry-level", "fresher", "trainee", "graduate", "intern"]

    text_lower = text.lower()
    
    senior_count = sum(1 for word in senior_keywords if word in text_lower)
    mid_count = sum(1 for word in mid_keywords if word in text_lower)
    junior_count = sum(1 for word in junior_keywords if word in text_lower)

    if senior_count > 0:
        return "Senior"
    elif mid_count > 0:
        return "Mid-level"
    elif junior_count > 0:
        return "Junior"
    else:
        # Default to Mid-level as per spec
        return "Mid-level"
