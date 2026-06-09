import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#050816,#0f172a);
}

.hero{
    text-align:center;
    padding:20px;
    animation:fadeUp 1.2s ease;
}


.hero h1{
    font-size:60px;
    font-weight:800;
    color:white;
}

.hero p{
    color:#94a3b8;
    font-size:20px;
}

@keyframes fadeUp{
    from{
        opacity:0;
        transform:translateY(40px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.stChatMessage{
    border-radius:20px;
    backdrop-filter:blur(10px);
}

.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    font-size:14px;
}
            [data-testid="stChatMessage"]{
    border-radius:20px;
    padding:15px;
    margin-bottom:10px;
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 8px 32px rgba(0,0,0,0.2);
}

[data-testid="stSidebar"]{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(15px);
}

body{
    background: linear-gradient(-45deg,#050816,#0f172a,#1e293b,#312e81);
    background-size:400% 400%;
    animation:gradientBG 15s ease infinite;
}

@keyframes gradientBG{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}
)
      </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:#94a3b8;font-size:18px'>
Career Guidance • Resume Review • Interview Prep • Roadmaps
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🤖 AI Career Assistant</h1>
    <p>Your AI-Powered Career Guide</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 👨‍💻 Developer")

st.sidebar.success("Amarjeet Srivastava")

st.sidebar.info("""


### Tech Stack
- Python
- Streamlit
- Gemini AI
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Connect")

st.sidebar.markdown(
    "[LinkedIn](https://www.linkedin.com)"
)

st.sidebar.markdown(
    "[GitHub](https://github.com)"
)

st.sidebar.markdown("""
### 🚀 Features

✅ Career Guidance

✅ Interview Preparation

✅ Resume Suggestions

✅ Download Chat

✅ AI Powered Responses
""")

uploaded_file = st.sidebar.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    st.sidebar.success("✅ Resume uploaded successfully")

    pdf = PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf.pages:
        resume_text += page.extract_text() + "\n"

    if st.sidebar.button("Analyze Resume"):

        with st.spinner("📄 Analyzing Resume..."):

            analysis_prompt = f"""
            Analyze this resume.

            Give:
            1. ATS Score out of 100
            2. Strengths
            3. Weaknesses
            4. Missing Skills
            5. Improvement Suggestions

            Resume:
            {resume_text}
            """

            result = model.generate_content(analysis_prompt)

            st.subheader("📊 Resume Analysis")
            st.write(result.text)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask about careers, interviews, resume building, skills..."
)

if prompt and prompt.strip():

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    with st.spinner("🤖 Thinking..."):
        try:
            response = model.generate_content(prompt.strip())
            reply = response.text

        except Exception as e:
            reply = f"Error: {e}"

    st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
st.markdown("""
<div class="footer">
Built with ❤️ using Streamlit & Gemini AI<br>
Developed by Amarjeet Srivastava
</div>
""", unsafe_allow_html=True)