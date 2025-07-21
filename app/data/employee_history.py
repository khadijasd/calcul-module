from typing import List, Dict
from datetime import datetime
from app.models.fiche_employee import Employee

class EmployeeHistory:
    def __init__(self):
        self.history = {}  # {employee_id: [{date: ..., skills: ...}]}
    
    def add_snapshot(self, employee: Employee):
        snapshot = {
            'date': datetime.now(),
            'skills': {s.skill_name: s.level_value for s in employee.actual_skills_level}
        }
        if employee.employee_id not in self.history:
            self.history[employee.employee_id] = []
        self.history[employee.employee_id].append(snapshot)
    
    def get_progress(self, employee_id: str, skill: str) -> List[Dict]:
        return [
            {'date': s['date'], 'level': s['skills'].get(skill, 0)}
            for s in self.history.get(employee_id, [])
            if skill in s['skills']
        ]