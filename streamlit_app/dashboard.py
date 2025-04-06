import streamlit as st
import pandas as pd
import requests
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.llm_utils.goal_parser import parse_goal_with_llm
from app.llm_utils.goal_parser import parse_goal_with_rag_fallback

st.title("💰 FinPilot AI - Smart Financial Planner")

# Common income input
income = st.number_input("Enter Monthly Income", min_value=0.0, step=100.0)

# --- CSV Upload Section ---
st.header("📂 Upload Expenses CSV")
csv_file = st.file_uploader("Upload a CSV with 'Description' and 'Amount' columns", type=["csv"])

if csv_file and st.button("Generate Plan from CSV"):
    files = {"file": csv_file.getvalue()}
    response = requests.post(
        f"http://localhost:8000/generate-plan-file/?income={income}",
        files={"file": csv_file}
    )
    if response.status_code == 200:
        data = response.json()
        st.success(f"Surplus: ${data['surplus']:.2f}")
        st.json(data["plan"])
    else:
        st.error("Error generating plan from CSV.")

# --- Manual Entry Section ---
st.header("📝 Manually Add Expenses")

with st.form("manual_expenses_form"):
    desc = st.text_input("Expense Description", "")
    amt = st.number_input("Amount", min_value=0.0, step=1.0)
    add_clicked = st.form_submit_button("Add Expense")

# Initialize buffers if not already
if "expense_buffer" not in st.session_state:
    st.session_state.expense_buffer = []

if "goal_buffer" not in st.session_state:
    st.session_state.goal_buffer = []

# Append to buffer
if add_clicked and desc and amt:
    st.session_state.expense_buffer.append({"description": desc, "amount": amt})

# Show current expenses
if st.session_state.expense_buffer:
    st.subheader("Entered Expenses")
    st.table(pd.DataFrame(st.session_state.expense_buffer))

# Button to generate plan
if st.button("Generate Plan from Manual Entry"):
    if not st.session_state.goal_buffer:
        st.warning("⚠️ Please add at least one goal before generating the plan.")
    elif not st.session_state.expense_buffer:
        st.warning("⚠️ Please add at least one expense before generating the plan.")
    else:
        payload = {
            "income": income,
            "expenses": st.session_state.expense_buffer,
            "goals": st.session_state.goal_buffer
        }

        # Debug print
        st.write("📤 Sending this payload to FastAPI:")
        st.json(payload)

        # Send request
        try:
            response = requests.post(
                "http://localhost:8000/generate-plan-manual/",
                json=payload
            )
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Surplus: ${data['surplus']:.2f}")
                st.subheader("🎯 Investment Plan")
                st.json(data["plan"])
            else:
                st.error(f"🚫 Error: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"❌ Request failed: {str(e)}")


st.header("🧠 Smart Goal Input")
goal_text_input = st.text_area(
    "Enter your financial goals (e.g. 'I want to save $5000 for a vacation in 12 months and $10000 for a car in 20 months')",
    ""
)

if st.button("Parse Goal"):
    with st.spinner("Thinking..."):
        parsed_text = parse_goal_with_rag_fallback(goal_text_input)
        try:
            parsed_goal = json.loads(parsed_text)

            if "goal_buffer" not in st.session_state:
                st.session_state.goal_buffer = []

            # ✅ Check if parsed_goal is a dict with a 'goals' key (common LLM format issue)
            if isinstance(parsed_goal, dict) and "goals" in parsed_goal:
                st.session_state.goal_buffer.extend(parsed_goal["goals"])
            elif isinstance(parsed_goal, list):
                st.session_state.goal_buffer.extend(parsed_goal)
            elif isinstance(parsed_goal, dict):
                st.session_state.goal_buffer.append(parsed_goal)
            else:
                st.error("⚠️ Unexpected response format from LLM.")
                st.code(parsed_text)

        except Exception as e:
            st.error("Could not parse the response as JSON.")
            st.code(parsed_text)
            st.exception(e)