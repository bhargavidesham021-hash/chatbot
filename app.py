import streamlit as st
import ollama

# Page configuration
st.set_page_config(
    page_title="AI Viva Practice Room",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Viva Practice Room")
st.write("Practice your project viva with AI using Ollama 3.2.")


# Session State
if "started" not in st.session_state:
    st.session_state.started = False

if "question_number" not in st.session_state:
    st.session_state.question_number = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "total_score" not in st.session_state:
    st.session_state.total_score = 0

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "last_score" not in st.session_state:
    st.session_state.last_score = 0


# Ollama function
def ask_ollama(prompt):
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# Project Details
if not st.session_state.started:

    st.subheader("📋 Enter Your Project Details")

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    project_title = st.text_input(
        "Project Title",
        placeholder="Example: Password Strength Analyzer"
    )

    project_description = st.text_area(
        "Project Description",
        placeholder="Explain your project briefly...",
        height=150
    )

    if st.button("▶️ Start Viva", use_container_width=True):

        if not student_name or not project_title or not project_description:
            st.warning("Please fill in all the project details.")

        else:

            st.session_state.student_name = student_name
            st.session_state.project_title = project_title
            st.session_state.project_description = project_description

            st.session_state.started = True
            st.session_state.question_number = 1

            prompt = f"""
You are an AI college viva examiner.

Student Name:
{student_name}

Project Title:
{project_title}

Project Description:
{project_description}

Generate ONE simple viva question specifically related to this project.

Ask only the question.
Do not give the answer.
Do not number the question.
"""

            st.session_state.current_question = ask_ollama(prompt)

            st.rerun()


# Viva Section
else:

    st.subheader(
        f"👩‍🎓 Student: {st.session_state.student_name}"
    )

    st.write(
        f"📚 Project: {st.session_state.project_title}"
    )

    st.divider()

    st.subheader(
        f"❓ Question {st.session_state.question_number}"
    )

    st.info(st.session_state.current_question)

    answer = st.text_area(
        "✍️ Your Answer",
        placeholder="Type your answer here...",
        height=150
    )

    if st.button(
        "✅ Submit Answer",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning(
                "Please enter your answer before submitting."
            )

        else:

            evaluation_prompt = f"""
You are a college project viva examiner.

Project Title:
{st.session_state.project_title}

Project Description:
{st.session_state.project_description}

Viva Question:
{st.session_state.current_question}

Student Answer:
{answer}

Evaluate the student's answer.

Give the response in exactly this format:

Score: X/10
Feedback: short and simple feedback

Give a score between 0 and 10.
"""

            evaluation = ask_ollama(evaluation_prompt)

            st.session_state.feedback = evaluation

            score = 0

            try:
                score_text = evaluation.split("Score:")[1]
                score_text = score_text.split("/10")[0]
                score = int(score_text.strip())

            except:
                score = 0

            st.session_state.last_score = score
            st.session_state.total_score += score


    # Show Feedback
    if st.session_state.feedback:

        st.subheader("📊 AI Evaluation")

        st.write(st.session_state.feedback)

        st.divider()

        st.write(
            f"⭐ Current Score: "
            f"{st.session_state.last_score}/10"
        )

        # Next question
        if st.session_state.question_number < 5:

            if st.button(
                "➡️ Next Question",
                use_container_width=True
            ):

                st.session_state.question_number += 1

                question_prompt = f"""
You are a college viva examiner.

Project Title:
{st.session_state.project_title}

Project Description:
{st.session_state.project_description}

Generate ONE new viva question.

The question should be different from previous questions
and should test the student's understanding of the project.

Ask only the question.
Do not give the answer.
"""

                st.session_state.current_question = ask_ollama(
                    question_prompt
                )

                st.session_state.feedback = ""

                st.rerun()

            if st.button("🔄 Change Project"):

                st.session_state.clear()

                st.rerun()

        else:

            st.success("🎉 Viva Completed!")

            st.subheader("📊 Final Result")

            st.write(
                f"Total Score: "
                f"{st.session_state.total_score}/50"
            )

            percentage = (
                st.session_state.total_score / 50
            ) * 100

            st.write(
                f"Performance: {percentage:.1f}%"
            )

            if percentage >= 80:

                st.success(
                    "Excellent performance! 🌟"
                )

            elif percentage >= 60:

                st.info(
                    "Good performance! Keep practicing. 👍"
                )

            elif percentage >= 40:

                st.warning(
                    "Average performance. More practice is recommended."
                )

            else:

                st.error(
                    "You need more preparation. Keep practicing!"
                )

            if st.button("🔄 Start New Viva"):

                st.session_state.clear()

                st.rerun()
