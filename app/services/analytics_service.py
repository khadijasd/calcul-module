# app/services/analytics_service.py
import numpy as np
from typing import List, Dict
from app.models.result import Result

def compute_global_statistics(results: List[Result]) -> Dict:
    if not results:
        return {
            "average_score": 0,
            "std_deviation": 0,
            "most_missing_skills": []
        }

    scores = [r.total_score for r in results]
    avg_score = sum(scores) / len(scores)
    std_dev = np.std(scores)

    # Compter les compétences manquantes
    common_gaps = {}
    for r in results:
        for detail in r.skill_gap_details:
            if detail.gap < 0:
                common_gaps[detail.skill_name] = common_gaps.get(detail.skill_name, 0) + 1

    top_missing_skills = sorted(common_gaps.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "average_score": round(avg_score, 2),
        "std_deviation": round(std_dev, 2),
        "most_missing_skills": top_missing_skills
    }
