from pydantic import BaseModel
from typing import List

class ExpenseItem(BaseModel):
    description: str
    amount: float

class Goal(BaseModel):
    name: str
    target_amount: float
    duration_months: int

class ManualExpensesRequest(BaseModel):
    income: float
    expenses: List[ExpenseItem]
    goals: List[Goal]

class PlanResponse(BaseModel):
    surplus: float
    plan: dict

