import re

import streamlit as st
import ollama


# Page configuration
st.set_page_config(
    page_title="AI Viva Practice Room",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 AI Viva Practice Room")
st.write("Practice your project viva with Ollama (llama3.2).")


def ask_ai(prompt):
    """Send a prompt to the local Ollama llama3.2 model."""
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as error:
        raise RuntimeError(
            "Could not reach Ollama. Make sure Ollama is running and the "
            "llama3.2 model is installed."
        ) from error

    answer = response["message"]["content"].strip()
    if not answer:
        raise RuntimeError("The AI service returned an empty response.")
    return answer


def generate_question(previous_questions=None):
    previous_questions = previous_questions or []
    previous_text = "\n".join(f"- {question}" for question in previous_questions)
    prompt = f"""
You are an AI college viva examiner.

Student Name:
{st.session_state.student_name}

Project Title:
{st.session_state.project_title}

Project Description:
{st.session_state.project_description}

Generate ONE simple viva question specifically related to this project.
The question must be different from these previous questions:
{previous_text or "None"}

Ask only the question. Do not give the answer or number the question.
"""
    return ask_ai(prompt)


def evaluate_answer(answer):
    prompt = f"""
You are a college project viva examiner.

Project Title:
{st.session_state.project_title}

Project Description:
{st.session_state.project_description}

Viva Question:
{st.session_state.current_question}

Student Answer:
{answer}

Evaluate the student's answer. Give a score from 0 to 10 and short,
simple feedback. Use exactly this format:
Score: X/10
Feedback: short feedback
"""
    return ask_ai(prompt)


def parse_score(evaluation):
    match = re.search(r"Score\s*:\s*(\d+)\s*/\s*10", evaluation, re.IGNORECASE)
    return min(10, int(match.group(1))) if match else 0


# Session state
if "started" not in st.session_state:
    st.session_state.started = False
if "question_number" not in st.session_state:
    st.session_state.question_number = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "previous_questions" not in st.session_state:
    st.session_state.previous_questions = []
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "last_score" not in st.session_state:
    st.session_state.last_score = 0


# Project details
if not st.session_state.started:
    st.subheader("📋 Enter Your Project Details")

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name",
    )
    project_title = st.text_input(
        "Project Title",
        placeholder="Example: Password Strength Analyzer",
    )
    project_description = st.text_area(
        "Project Description",
        placeholder="Explain your project briefly...",
        height=150,
    )

    if st.button("▶️ Start Viva", width="stretch"):
        if not student_name.strip() or not project_title.strip() or not project_description.strip():
            st.warning("Please fill in all the project details.")
        else:
            st.session_state.student_name = student_name.strip()
            st.session_state.project_title = project_title.strip()
            st.session_state.project_description = project_description.strip()
            try:
                question = generate_question()
            except Exception as error:
                st.error(f"Could not generate a question: {error}")
            else:
                st.session_state.current_question = question
                st.session_state.previous_questions = [question]
                st.session_state.started = True
                st.session_state.question_number = 1
                st.rerun()


# Viva section
else:
    st.subheader(f"👩‍🎓 Student: {st.session_state.student_name}")
    st.write(f"📚 Project: {st.session_state.project_title}")

    if st.button("🔄 Change Project"):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.subheader(f"❓ Question {st.session_state.question_number} of 5")
    st.info(st.session_state.current_question)

    if not st.session_state.feedback:
        answer = st.text_area(
            "✍️ Your Answer",
            placeholder="Type your answer here...",
            height=150,
            key=f"answer_{st.session_state.question_number}",
        )

        if st.button("✅ Submit Answer", width="stretch"):
            if not answer.strip():
                st.warning("Please enter your answer before submitting.")
            else:
                try:
                    evaluation = evaluate_answer(answer.strip())
                except Exception as error:
                    st.error(f"Could not evaluate the answer: {error}")
                else:
                    score = parse_score(evaluation)
                    st.session_state.feedback = evaluation
                    st.session_state.last_score = score
                    st.session_state.total_score += score
                    st.rerun()

    if st.session_state.feedback:
        st.subheader("📊 AI Evaluation")
        st.write(st.session_state.feedback)
        st.write(f"⭐ Current Score: {st.session_state.last_score}/10")

        if st.session_state.question_number < 5:
            if st.button("➡️ Next Question", width="stretch"):
                try:
                    question = generate_question(st.session_state.previous_questions)
                except Exception as error:
                    st.error(f"Could not generate the next question: {error}")
                else:
                    st.session_state.question_number += 1
                    st.session_state.current_question = question
                    st.session_state.previous_questions.append(question)
                    st.session_state.feedback = ""
                    st.session_state.last_score = 0
                    st.rerun()
        else:
            st.success("🎉 Viva Completed!")
            st.subheader("📊 Final Result")
            st.write(f"Total Score: {st.session_state.total_score}/50")

            percentage = (st.session_state.total_score / 50) * 100
            st.write(f"Performance: {percentage:.1f}%")

            if percentage >= 80:
                st.success("Excellent performance! 🌟")
            elif percentage >= 60:
                st.info("Good performance! Keep practicing. 👍")
            elif percentage >= 40:
                st.warning("Average performance. More practice is recommended.")
            else:
                st.error("You need more preparation. Keep practicing!")

            if st.button("🔄 Start New Viva"):
                st.session_state.clear()
                st.rerun()
