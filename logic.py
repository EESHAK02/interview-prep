# import json
# import uuid
# import time
# from datetime import datetime
# import os
# from PyPDF2 import PdfReader  # new dependency

# DATA_DIR = "data"
# SESSIONS_FILE = f"{DATA_DIR}/sessions.json"
# WEAKNESSES_FILE = f"{DATA_DIR}/weaknesses.json"
# RESUME_FILE = f"{DATA_DIR}/resume.txt"
# JD_FILE = f"{DATA_DIR}/jd.txt"

# # ---------------- PDF Resume ----------------
# def save_resume_pdf(uploaded_file):
#     """Parse PDF to text and save as resume.txt"""
#     reader = PdfReader(uploaded_file)
#     text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
#     os.makedirs(DATA_DIR, exist_ok=True)
#     with open(RESUME_FILE, "w", encoding="utf-8") as f:
#         f.write(text)
#     return text

# def load_resume():
#     """Load resume text safely; return empty string if not found."""
#     if os.path.exists(RESUME_FILE):
#         with open(RESUME_FILE, "r", encoding="utf-8") as f:
#             return f.read()
#     else:
#         return ""

# def save_job_description(jd_text):
#     """Save pasted JD to jd.txt"""
#     os.makedirs(DATA_DIR, exist_ok=True)
#     with open(JD_FILE, "w", encoding="utf-8") as f:
#         f.write(jd_text)
#     return jd_text

# def load_job_description():
#     try:
#         with open(JD_FILE, "r", encoding="utf-8") as f:
#             return f.read()
#     except:
#         return ""



# # ---------- Sessions ----------

# def load_sessions():
#     try:
#         with open(SESSIONS_FILE, "r") as f:
#             return json.load(f)
#     except:
#         return []


# def save_session(session):
#     sessions = load_sessions()
#     sessions.append(session)
#     with open(SESSIONS_FILE, "w") as f:
#         json.dump(sessions, f, indent=2)


# def create_session(
#     role,
#     difficulty,
#     question,
#     answer,
#     stress_mode,
#     time_taken_sec,
#     feedback,
#     weakness_tags
# ):
#     return {
#         "session_id": str(uuid.uuid4()),
#         "timestamp": datetime.now().isoformat(),
#         "role": role,
#         "difficulty": difficulty,
#         "question": question,
#         "answer": answer,
#         "stress_mode": stress_mode,
#         "time_taken_sec": time_taken_sec,
#         "feedback": feedback,
#         "weakness_tags": weakness_tags
#     }


# # ---------- Weaknesses ----------

# def load_weaknesses():
#     try:
#         with open(WEAKNESSES_FILE, "r") as f:
#             return json.load(f)
#     except:
#         return []


# def save_weakness(tag):
#     if not tag:
#         return
#     data = load_weaknesses()
#     data.append(tag)
#     with open(WEAKNESSES_FILE, "w") as f:
#         json.dump(data, f, indent=2)


# # ---------- Stress Mode ----------

# def start_timer():
#     return time.time()


# def end_timer(start_time):
#     return int(time.time() - start_time)


# # ---------- Progress Metrics ----------

# def compute_progress():
#     sessions = load_sessions()
#     if not sessions:
#         return {}

#     total = len(sessions)
#     avg_time = sum(s["time_taken_sec"] for s in sessions) / total
#     stress_count = sum(1 for s in sessions if s["stress_mode"])

#     weaknesses = {}
#     for s in sessions:
#         for w in s["weakness_tags"]:
#             weaknesses[w] = weaknesses.get(w, 0) + 1

#     return {
#         "total_sessions": total,
#         "average_time": round(avg_time, 1),
#         "stress_sessions": stress_count,
#         "weaknesses": weaknesses
#     }

def build_context(resume, jd, interviewer=None):
    ctx = f"""
Resume:
{resume}

Job Description:
{jd}
"""
    if interviewer:
        ctx += f"\nInterviewer Info:\n{interviewer}"

    return ctx
