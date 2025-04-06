import openai
from dotenv import load_dotenv
import json
load_dotenv()
import os
from app.rag.rag_loader import load_rag_db
# You can later set this via env vars for security

# Read API key securely
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize client
client = openai.OpenAI(api_key=openai_api_key)
vectordb = load_rag_db()

def build_goal_prompt(goal_text: str) -> str:
    return f"""
Extract all financial goals from the user's message.

Each goal must include:
- name
- target_amount (in USD)
- duration_months (in months)

Return the result as a JSON list — DO NOT wrap inside a "goals" key.

Example:
[
  {{
    "name": "Vacation",
    "target_amount": 5000,
    "duration_months": 12
  }},
  {{
    "name": "Car",
    "target_amount": 10000,
    "duration_months": 20
  }}
]

User input:
"{goal_text}"
"""

def parse_goal_with_llm(goal_text: str):
    prompt = f"""
You are a financial assistant. The user has not provided all the data.
Please estimate missing target_amount if needed.

Input: "{goal_text}"

Return JSON list like:
[
  {{
    "name": "Car",
    "target_amount": 10000,
    "duration_months": 12
  }}
]
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def save_goal_to_kb(goal_json: str, source_text: str):
    """
    Saves goal to context file for future RAG use.
    """
    try:
        goals = json.loads(goal_json)
        with open("data/context_docs.txt", "a") as f:
            for goal in goals:
                line = f"Goal: {goal['name']} | Amount: {goal['target_amount']} | Duration: {goal['duration_months']} months | Source: {source_text}\n"
                f.write(line)
        print("✅ Saved goal(s) to knowledge base.")
    except Exception as e:
        print(f"❌ Could not save to KB: {e}")

def parse_goal_with_rag_fallback(goal_text: str):
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(goal_text)

    if not docs:
        print("⚠️ No relevant context found — falling back to LLM only.")
        parsed_text = parse_goal_with_llm(goal_text)
        try:
            save_goal_to_kb(parsed_text, goal_text)
            global vectordb
            vectordb = load_rag_db()
            print("✅ Vector DB reloaded after saving new goal.")
        except Exception as e:
            print(f"❌ Could not auto-save fallback goal to KB: {e}")

        return parsed_text

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a financial assistant. Use the following context to interpret and estimate the user's financial goals.

Context:
{context}

User goal:
"{goal_text}"

Extract:
- name
- target_amount (estimate if missing)
- duration_months

Respond in this format:
[
  {{
    "name": "Vacation",
    "target_amount": 5000,
    "duration_months": 12
  }}
]
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
