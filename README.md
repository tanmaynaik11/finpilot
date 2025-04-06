# 💰 FinPilot AI - Smart Financial Planner

FinPilot AI is an intelligent financial planning assistant that helps users manage income, track expenses, set financial goals, and generate personalized investment plans — powered by **Machine Learning**, **LLMs (OpenAI)**, and **RAG (Retrieval-Augmented Generation)**. Built using **FastAPI**, **Streamlit**, and **ChromaDB**, this app runs locally and is designed to later support edge/mobile deployment.

---

## 🚀 Features

- ✅ Upload or manually input monthly expenses
- ✅ Classify expenses as fixed/variable using a custom ML model
- ✅ Input goals in natural language (e.g. "I want to save for a house in 20 months")
- ✅ Parse goals using LLM (GPT-3.5) and fallback to estimates when RAG fails
- ✅ Auto-learn new goals by saving them into the knowledge base
- ✅ Generate time-weighted investment plans based on surplus
- ✅ Visualize structured outputs in a clean, interactive Streamlit dashboard

---

## 🏗️ Tech Stack

| Component         | Tool/Library                      |
|------------------|-----------------------------------|
| Frontend          | Streamlit                         |
| Backend API       | FastAPI                           |
| ML Classifier     | scikit-learn (Logistic Regression)|
| LLM Integration   | OpenAI GPT-3.5                    |
| RAG Engine        | LangChain + ChromaDB              |
| Embeddings        | HuggingFace Transformers          |
| Storage           | Local filesystem / .env files     |

---

## 🧠 How It Works

1. User provides income and expenses (CSV or manually)
2. ML model classifies expenses (fixed vs variable)
3. Surplus is calculated → `Income - Total Expenses`
4. User enters financial goals in natural language
5. RAG tries to find related context from a knowledge base
6. If no RAG match is found, fallback to LLM estimation
7. Goals from fallback are automatically saved to the KB
8. A time-based investment plan is generated based on monthly need

---


