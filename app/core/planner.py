def generate_budget_plan(income, fixed, variable, goals):
    surplus = income - (fixed + variable)
    plan = {}

    # Calculate monthly need for each goal
    goal_needs = []
    for g in goals:
        monthly = g["target_amount"] / g["duration_months"]
        goal_needs.append((g["name"], monthly))

    total_monthly_need = sum([m for _, m in goal_needs])

    if total_monthly_need == 0:
        return {g["name"]: 0 for g in goals}

    # Proportional distribution
    for goal_name, monthly in goal_needs:
        allocation = (monthly / total_monthly_need) * surplus
        plan[goal_name] = round(allocation, 2)

    return plan
