import streamlit as st
from llm_utils import generate_question, evaluate_answer
from logic import build_context
from storage import log_session, log_weakness
from PyPDF2 import PdfReader
import json
from collections import Counter

st.set_page_config(page_title="Interview Prep", layout="wide")
st.title("Interview Prep")
st.subheader("Let's nail your next interview!")

# ---------- Helpers ----------

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# ---------- Sidebar ----------

st.sidebar.title("Profile Setup")

resume_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.sidebar.text_area("Paste Job Description")
interviewer_info = st.sidebar.text_area("Interviewer Info (Optional)")

if resume_file:
    resume_text = extract_text_from_pdf(resume_file)
else:
    resume_text = ""

context = build_context(resume_text, jd_text, interviewer_info)

# ---------- Tabs ----------

tabs = st.tabs(["Prep Hub", "Mock Interview", "Progress"])

# ================= PREP HUB =================

with tabs[0]:
    st.header("Prep Hub")

    mode = st.radio("Mode", ["Conceptual", "Behavioral", "Coding", "Mixed"])
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    if st.button("Generate Question"):
        chosen_mode = mode if mode != "Mixed" else "Conceptual"
        q = generate_question(context, chosen_mode, difficulty)
        st.session_state.current_question = q

    if st.session_state.current_question:
        st.subheader("Question")
        st.write(st.session_state.current_question)

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            feedback = evaluate_answer(context, st.session_state.current_question, answer)
            st.subheader("Feedback")
            st.write(feedback)

            log_session({
                "mode": mode,
                "difficulty": difficulty,
                "question": st.session_state.current_question,
                "answer": answer,
                "feedback": feedback
            })

# ================= MOCK INTERVIEW =================


with tabs[1]:
    st.header("Mock Interview")

    duration = st.slider("Interview Duration (mins)", 15, 90, 30)
    mix = st.multiselect(
        "Question Mix",
        ["Conceptual", "Behavioral", "Coding"],
        default=["Conceptual", "Behavioral"]
    )

    # Initialize state
    if "mock_question" not in st.session_state:
        st.session_state.mock_question = None
    if "mock_answer" not in st.session_state:
        st.session_state.mock_answer = ""
    if "mock_feedback" not in st.session_state:
        st.session_state.mock_feedback = None
    if "mock_counter" not in st.session_state:
        st.session_state.mock_counter = 0

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start / Next Question", key="mock_next"):
            mode = mix[st.session_state.mock_counter % len(mix)] if mix else "Conceptual"
            st.session_state.mock_question = generate_question(context, mode, "Medium")
            st.session_state.mock_answer = ""
            st.session_state.mock_feedback = None
            st.session_state.mock_counter += 1

    with col2:
        if st.button("Reset Mock Interview", key="mock_reset"):
            st.session_state.mock_question = None
            st.session_state.mock_answer = ""
            st.session_state.mock_feedback = None
            st.session_state.mock_counter = 0

    if st.session_state.mock_question:
        st.subheader(f"Question {st.session_state.mock_counter}")
        st.write(st.session_state.mock_question)

        st.session_state.mock_answer = st.text_area(
            "Your Answer",
            value=st.session_state.mock_answer,
            key="mock_answer_box"
        )

        if st.button("Submit Answer", key="mock_submit"):
            st.session_state.mock_feedback = evaluate_answer(
                context,
                st.session_state.mock_question,
                st.session_state.mock_answer
            )

    if st.session_state.mock_feedback:
        st.subheader("Feedback")
        st.write(st.session_state.mock_feedback)


# # ================= PROGRESS =================

with tabs[2]:
    st.header("Progress")

    # Load last 5 sessions from JSON
    try:
        with open("data/sessions.json", "r", encoding="utf-8") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = []

    sessions_to_display = sessions[-5:]  # Last 5 sessions

    if not sessions_to_display:
        st.info("No past sessions found.")
    else:
        # Extract all strengths, weaknesses, improvements
        all_strengths = []
        all_weaknesses = []
        all_improvements = []

        for s in sessions_to_display:
            fb = s.get("feedback", "")
            # Heuristic splitting based on format
            if "Strengths:" in fb:
                str_sec = fb.split("Strengths:")[1].split("Weaknesses:")[0].strip().split("\n")
                all_strengths.extend([x.strip("- ").strip() for x in str_sec if x.strip()])
            if "Weaknesses:" in fb:
                weak_sec = fb.split("Weaknesses:")[1].split("What could be improved:")[0].strip().split("\n")
                all_weaknesses.extend([x.strip("- ").strip() for x in weak_sec if x.strip()])
            if "What could be improved:" in fb:
                imp_sec = fb.split("What could be improved:")[1].split("A stronger sample answer:")[0].strip().split("\n")
                all_improvements.extend([x.strip("- ").strip() for x in imp_sec if x.strip()])

        # Function to get top 3 most common points
        def top3(items):
            count = Counter(items)
            return [x for x, _ in count.most_common(3)]

        top_strengths = top3(all_strengths)
        top_weaknesses = top3(all_weaknesses)
        top_improvements = top3(all_improvements)

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Questions Answered", sum(1 for s in sessions_to_display))
        col2.metric("Sessions Completed", len(sessions_to_display))
        col3.metric("Modes Covered", len(set(s.get("mode", "Unknown") for s in sessions_to_display)))

        st.markdown("---")

        # Display top points with color coding
        def display_points(title, points, color):
            st.markdown(f"### {title}")
            for p in points:
                st.markdown(f"<span style='color:{color}'>• {p}</span>", unsafe_allow_html=True)

        display_points("Top 3 Strengths", top_strengths, "green")
        display_points("Top 3 Weaknesses", top_weaknesses, "red")
        display_points("Top 3 Areas for Improvement", top_improvements, "orange")

#     try:
#         import json
#         with open("data/sessions.json", "r", encoding="utf-8") as f:
#             sessions = json.load(f)

#         st.write("Total Questions Answered:", len(sessions))

#         for s in sessions[-5:]:
#             st.markdown("----")
#             st.write("Mode:", s["mode"])
#             st.write("Q:", s["question"])
#             st.write("Feedback:", s["feedback"])

#     except:
#         st.info("No sessions yet.")
