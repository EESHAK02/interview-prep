import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:latest"

def call_llm(prompt, temperature=0.7):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }

    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()
    return r.json()["response"].strip()


def generate_question(context, mode, difficulty):
    prompt = f"""
You are an interview coach.

Context:
{context}

Mode: {mode}
Difficulty: {difficulty}

Ask ONE clear interview question.
No explanations.
"""

    if mode == "Conceptual":
        prompt += "\nFocus on theory, tradeoffs, systems."
    elif mode == "Behavioral":
        prompt += "\nAsk STAR-style behavioral question."
    elif mode == "Coding":
        prompt += "\nAsk a practical coding task, not LeetCode style."

    return call_llm(prompt)


def evaluate_answer(context, question, answer):
    prompt = f"""
You are acting as a strict interview evaluator.

IMPORTANT RULES:
- Do NOT comment on the candidate's resume or background.
- Do NOT mention their profile, education, or past work.
- Evaluate ONLY the given answer to the given question.
- Assume no prior knowledge about the candidate.
- Be specific, concrete, and actionable.

Question:
{question}

Candidate's Answer:
{answer}

Give feedback in this format:

Strengths:
- ...

Weaknesses:
- ...

What could be improved:
- ...

A stronger sample answer:
- ...
"""

    return call_llm(prompt, temperature=0.2)

