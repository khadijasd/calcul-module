from typing import List, Dict
import requests

class TrainingRepository:
    def __init__(self):
        self.local_catalog = {
    "Python": {
        3: [{"id": "py3", "name": "Python Intermediate", "duration": "20h", "tags": ["data"]}],
        4: [{"id": "py4", "name": "Python Advanced", "duration": "30h", "tags": ["web", "data"]}]
    },
    "SQL": {
        2: [{"id": "sql2", "name": "SQL Basics", "duration": "15h", "tags": ["database"]}]
    },
    "Data Science": {
        3: [{"id": "ds3", "name": "Intro to Data Science", "duration": "25h", "tags": ["data", "ml"]}]
    }
}


    def get_courses(self, skill_name: str, min_level: int, max_level: int) -> List[Dict]:
        courses = []
        # Local
        courses.extend(self._get_local_courses(skill_name, min_level, max_level))
        
        # Externe (exemple)
        try:
            courses.extend(self._get_external_courses(skill_name, min_level, max_level))
        except Exception:
            pass
        return courses

    def _get_local_courses(self, skill_name: str, min_level: int, max_level: int) -> List[Dict]:
        result = []
        for level in range(min_level, max_level + 1):
            if skill_name in self.local_catalog and level in self.local_catalog[skill_name]:
                for course in self.local_catalog[skill_name][level]:
                    course_copy = course.copy()
                    course_copy["level"] = level
                    course_copy["source"] = "local"
                    result.append(course_copy)
        return result

    def _get_external_courses(self, skill_name: str, min_level: int, max_level: int) -> List[Dict]:
        response = requests.get(
            "https://api.udemy.com/courses",
            params={
                "search": skill_name,
                "min_level": min_level,
                "max_level": max_level
            }
        )
        return [
            {
                "id": c["id"],
                "name": c["title"],
                "level": c["level"],
                "duration": c["duration"],
                "tags": c.get("tags", []),
                "source": "udemy"
            }
            for c in response.json()["results"]
        ]
        
        
    def get_all_courses(self) -> List[Dict]:
     courses = []
     for skill_name, levels in self.local_catalog.items():
        for level, level_courses in levels.items():
            for course in level_courses:
                course_copy = course.copy()
                course_copy["skill_name"] = skill_name
                course_copy["level"] = level
                course_copy["source"] = "local"
                courses.append(course_copy)
     return courses
