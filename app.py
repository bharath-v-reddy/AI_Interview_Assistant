import streamlit as st
from groq import Groq

st.set_page_config(page_title='LLM', layout='centered')

st.title('AI Interview')
st.caption('Practice and Prepare for your placement')
st.caption('BHARATH V REDDY')

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Advanced Settings.")
    st.stop()
role = st.selectbox("Job Title", ["Machine Learning Engineer", "Senior Software Engineering", "Full Stack Engineer", "Backend Engineer", "Others"])

if role =="Others":
    st.text_input("Enter your Job Title","XXXXXX")
model = st.selectbox(
    "Choose Your Model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
)
level=st.selectbox(
    "Choose your level",
    [
        "Beginner", "Intermediate", "Advanced"
    ]
)
mode = st.radio("Activity",["General Question", "Generate Code Questions", "Evaluate Answers", "Improve Answer"])
if mode =="Generate Question" :
    count = st.slider("Number Of Questions",1,10,5)
elif mode =="Generate code Questions" :
    topic = st.selectbox( "Select Topic",
                         [ "Python", "C++", "C", "DSA", "Aptitude", "Java"])
    count= st.slider("Number of Questions",1,10,5)
else:
    question = st.text_area("Enter Interview Question Here")
    answer = st.text_area("Enter Your Answer", height=160)

if st.button("Generate AI Response", type = "primary") :
    if mode == ["Evaluate Answer", "Improve Answer"] and (not question.strip()) or (not answer.strip()):
        st.warning ("Please enter a valid Question and Answer")
        st.stop()
        
topics = "Topic is" + topic +"Difficulty is" +level
    if mode == "Generate Question" :
        task = "Generate" + str(count) +"Frequently asked Interview question 3 situation based questions as well as 2 theory questions"
    elif mode == "Generate Code Questions":
        task="Generate" +str(count) + "Frequently asked Coding or technical questions for the topics"+ topic + "and give me the hints with accurate performance."
    elif mode == "Evaluate Answers":
        task = "Question:"+ question + "Answer: "+answer+"Evaluate the answer based on the question and identify the drawbacks ."
    elif mode == "Improve Answer" :
        task = "Question:" = question + "Answer: " + answer + "Improve the answer based on the result and highligth the important points."
        backround = "Job Role :" +role + "Difficulty level" +level 
    with st.spinner("Generating Your answer....."):
        try:
            req = client.chat.completions.create (
    model=  gen_model , 
    messages =[
        {"role" : "system", "content" : " Act as You are an expert Technical Interviewer as well the HR "},
        {
            "role" : "user", "content" : backround + task
        }

    ],
    temperature = 0.7,
    max_tokens = 1800 
           output = req.choices[0].message.content
    st.subheader("AI Response" )
    st.markdown(output)
    st.download_button("Download Response", output , file_name = "Interview_Response.txt", mine ="text/plain")
            )
        except Exception as e:
            st.error ("API connection was unsuccessful:", e)
            st.info("Please check your API keys and rate limits :")
