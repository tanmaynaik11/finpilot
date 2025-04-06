from fastapi import APIRouter
import pandas as pd
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.schemas.models import ManualExpensesRequest
from app.ml_models.classifier import classify_expenses
from app.core.planner import generate_budget_plan
from app.schemas.models import ManualExpensesRequest

router = APIRouter()

# @router.post("/classify")
# def classify(txn: Transaction):
#     category = classify_transaction(txn.description, txn.amount)
#     return {"category": category}

# @router.post("/plan")
# def plan(profile: UserProfile):
#     plan = generate_budget_plan(
#         profile.income,
#         profile.fixed_expenses,
#         profile.variable_expenses,
#         profile.goals
#     )
#     return {"plan": plan}
@router.post("/generate-plan-file/")
async def generate_plan(income: float, file: UploadFile = File(None)):
    if file:
        df = pd.read_csv(file.file)
    else:
        return JSONResponse({"error": "No file uploaded."}, status_code=400)

    df = classify_expenses(df)
    fixed = df[df["category"] == "Fixed"]["Amount"].sum()
    variable = df[df["category"] == "Variable"]["Amount"].sum()
    surplus = income - (fixed + variable)

    plan = generate_budget_plan(income, fixed, variable, ["Emergency Fund", "Retirement", "Vacation"])
    return {
        "surplus": surplus,
        "plan": plan
    }

@router.post("/generate-plan-manual/")
async def generate_plan_manual(payload: ManualExpensesRequest):
    try:
        df = pd.DataFrame([e.dict() for e in payload.expenses])
        df.rename(columns={"description": "Description", "amount": "Amount"}, inplace=True)

        print("🧾 Parsed Expenses:")
        print(df)

        df = classify_expenses(df)

        fixed = df[df["category"] == "Fixed"]["Amount"].sum()
        variable = df[df["category"] == "Variable"]["Amount"].sum()
        surplus = payload.income - (fixed + variable)

        print("✅ Calculated Surplus:", surplus)

        # Extract goal names for planner
        goal_dicts = [goal.dict() for goal in payload.goals]
        print("🎯 Goals Received:", goal_dicts)

        plan = generate_budget_plan(payload.income, fixed, variable, goal_dicts)

        return {
            "surplus": surplus,
            "plan": plan,
            "goals_used": goal_dicts
        }

    except Exception as e:
        print("❌ Error in generate-plan-manual:", str(e))
        raise e
