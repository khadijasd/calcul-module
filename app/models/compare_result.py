from typing import List
from pydantic import BaseModel
from app.models.result import Result

class CompareResult(BaseModel):
    employee_id: int
    name: str
    position: str
    results_by_method: dict  # key: method name, value: Result
