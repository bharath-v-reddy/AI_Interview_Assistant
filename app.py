
import streamlit as st
from groq import Groq

st.set_page_config(page_title="LLM", layout="centered")

st.title("AI Interview")
st.caption("Practice and Prepare for your placement")
st.caption("BHARATH V REDDY")


try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Advanced Settings.")
    st.stop()


role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "Full Stack Engineer",
        "Backend Engineer",
        "Others"
    ]
)

if role == "Others":
    custom_role = st.text_input("Enter Your Job Title", "XXXXXX")
    role = custom_role

model = st.selectbox(
    "Choose Your Model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)


level = st.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
)


mode = st.radio(
    "Activity",
    [
        "General Question",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answer"
    ]
)


if mode == "General Question":
    count = st.slider("Number of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":
    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"]
    )
    count = st.slider("Number of Questions", 1, 10, 5)

else:
    question = st.text_area("Enter Interview Question Here")
    answer = st.text_area("Enter Your Answer", height=160)


if st.button("Generate AI Response", type="primary"):
    
    if mode in ["Evaluate Answers", "Improve Answer"]:
        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid Question and Answer")
            st.stop()

    background = (
        "Job Role: " + role +
        "\nDifficulty Level: " + level
    )

    if mode == "General Question":
        task = (
            "Generate " + str(count) +
            " frequently asked interview questions for this job role. "
            "Include situation-based questions and theory questions. "
            "Provide answers for all questions."
        )

    elif mode == "Generate Code Questions":
        task = (
            "Generate " + str(count) +
            " frequently asked coding or technical interview questions "
            "for the topic " + topic +
            ". Include hints and answers with explanations."
        )

    elif mode == "Evaluate Answers":
        task = (
            "Question: " + question +
            "\nAnswer: " + answer +
            "\nEvaluate the answer based on the question. "
            "Identify the drawbacks, missing concepts, strengths, "
            "and provide a score out of 10."
        )

    elif mode == "Improve Answer":
        task = (
            "Question: " + question +
            "\nAnswer: " + answer +
            "\nImprove the answer to make it suitable for an interview. "
            "Highlight important points and provide a clear, "
            "professional answer."
        )

   
    with st.spinner("Generating Your Answer....."):
        try:
            req = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Technical Interviewer "
                            "and HR professional. Give accurate, clear, "
                            "structured, and student-friendly answers."
                        )
                    },
                    {
                        "role": "user",
                        "content": background + "\n" + task
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = req.choices[0].message.content

            st.subheader("AI Response")
            st.markdown(output)

            st.download_button(
                "Download Response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API connection was unsuccessful: {e}")
            st.info("Please check your API key and rate limits.")
