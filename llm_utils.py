# import subprocess

# # ---------------- DEFAULT MODEL ----------------
# DEFAULT_MODEL = "llama3.1"

# # ---------------- CORE QUERY FUNCTION ----------------
# def query_ollama(prompt, model=DEFAULT_MODEL):
#     """
#     Run Ollama safely with UTF-8 encoding on Windows and Linux.
#     """
#     try:
#         # Send prompt as UTF-8 bytes
#         result = subprocess.run(
#             ["ollama", "run", model],
#             input=prompt.encode("utf-8"),  # encode to UTF-8
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE
#         )

#         # Decode outputs
#         output = result.stdout.decode("utf-8").strip()
#         error = result.stderr.decode("utf-8").strip()

#         if error:
#             print("Ollama error:", error)

#         return output
#     except Exception as e:
#         print("Error running Ollama:", e)
#         return "Error: Could not generate output"

# # ---------------- QUESTION GENERATION ----------------
# def generate_question(resume_text, jd_text, role, difficulty):
#     """
#     Generate a single interview question based on resume + JD.
#     """
#     prompt = f"""
# You are an interviewer hiring for a {role} role.

# Use the candidate's resume and the job description to create ONE {difficulty} difficulty interview question.

# Resume:
# {resume_text}

# Job Description:
# {jd_text}

# Return only the question text, no extra commentary.
# """
#     return query_ollama(prompt)

# # ---------------- CONCEPT EXPLANATION ----------------
# def generate_concept_explanation(resume_text, jd_text, topic, depth="High-level"):
#     """
#     Generate a concept explanation or key talking points, grounded in resume and JD.
#     """
#     prompt = f"""
# You are a subject matter expert helping a candidate prepare for a role.

# Resume:
# {resume_text}

# Job Description:
# {jd_text}

# Topic to explain: {topic}
# Depth: {depth}

# Generate a concise, structured explanation suitable for interview preparation.
# Include key talking points and insights that align with the role.
# """
#     return query_ollama(prompt)

# # ---------------- BEHAVIORAL ANSWER REFINEMENT ----------------
# def generate_behavioral_answer(resume_text, jd_text, question_type, draft_answer):
#     """
#     Refine a behavioral answer using the candidate's resume and JD context.
#     """
#     prompt = f"""
# You are an experienced interviewer.

# Resume:
# {resume_text}

# Job Description:
# {jd_text}

# Behavioral question type: {question_type}
# Candidate draft answer: {draft_answer}

# Provide a polished, structured, and concise answer that is role- and JD-specific.
# """
#     return query_ollama(prompt)

# # ---------------- FEEDBACK / EVALUATION ----------------
# def evaluate_answer(question, answer):
#     """
#     Evaluate a candidate answer and provide structured feedback.
#     """
#     prompt = f"""
# You are an experienced interviewer.

# Question:
# {question}

# Candidate answer:
# {answer}

# Provide structured feedback:
# 1. Strengths
# 2. Gaps
# 3. One concrete improvement

# Be concise and direct.
# """
#     return query_ollama(prompt)

# # ---------------- OPTIONAL ANSWER REFINEMENT ----------------
# def refine_answer(answer):
#     """
#     Improve a generic answer, making it concise, structured, and impactful.
#     """
#     prompt = f"""
# Improve this interview answer.
# Make it concise, structured, and impactful.

# Answer:
# {answer}
# """
#     return query_ollama(prompt)

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

