from typing import Dict, List

TRAINING_DATABASE: Dict[str, Dict[int, Dict]] = {
    "Python": {
        1: {
            "course_id": "PY101",
            "name": "Python Fundamentals",
            "duration": "2 weeks",
            "provider": "Internal Academy",
            "link": "/training/PY101"
        },
        2: {
            "course_id": "PY201",
            "name": "Python for Data Analysis",
            "duration": "3 weeks",
            "prerequisite": "PY101",
            "provider": "DataCamp",
            "link": "https://datacamp.com/PY201"
        },
        3: {
            "course_id": "PY301",
            "name": "Advanced Python Patterns",
            "duration": "4 weeks",
            "provider": "Internal Expert",
            "certification": True
        }
    },
    "React": {
        1: {
            "course_id": "RE101",
            "name": "React Basics",
            "duration": "2 weeks",
            "type": "video-course",
            "platform": "Pluralsight"
        },
        2: {
            "course_id": "RE201",
            "name": "State Management",
            "duration": "3 weeks",
            "hands_on_labs": True
        }
    },
    "Machine Learning": {
        1: {
            "course_id": "ML101",
            "name": "ML Fundamentals",
            "duration": "4 weeks",
            "math_prerequisite": True
        }
    }
}

SKILL_ALIASES = {
    "PY": "Python",
    "ReactJS": "React",
    "ML": "Machine Learning"
}

def get_course(skill_name: str, level: int) -> Dict | None:
    """Helper to access courses with skill name normalization"""
    skill_name = SKILL_ALIASES.get(skill_name, skill_name)
    return TRAINING_DATABASE.get(skill_name, {}).get(level)