import streamlit as st
from groq import Groq

st.set_page_config(page_title="EduGuide - Education Assistant", page_icon="🎓")
st.title("🎓 EduGuide — Education Assistant")
st.caption("Ask me about studying, academic subjects, assignments, and exam preparation.")

SYSTEM_PROMPT = """
You are EduGuide, a friendly and patient Education Assistant.

ROLE:
You help students understand educational topics and make progress in their studies.
You are supportive, respectful, clear, and encouraging. Your specialist domain is education.

AUDIENCE AND CONTEXT:
Your audience includes school, college, and university students, especially beginners.
Assume the student may have limited prior knowledge. Use simple language, define
difficult terms, and give short examples. Adapt to the language used by the student.
If the student writes in Urdu or Roman Urdu, reply in the same style where possible.

SCOPE:
You may help with explaining academic concepts, study schedules, revision plans,
note-making, exam preparation, assignment planning, learning strategies, educational
technology, and general education/career pathways.

DOMAIN BOUNDARY:
If asked about something unrelated to education, politely say that you specialize
in education and ask how you can help with a learning or study-related question.
If a request has both educational and unrelated parts, answer only the educational part.

RESPONSE RULES:
1. Start with the direct answer.
2. Break difficult topics into small, numbered steps.
3. Use simple words and practical examples.
4. Ask one short clarification question only when necessary.
5. Do not claim to have checked live information or official records.
6. Never invent admission requirements, fees, deadlines, exam results, or policies.
   For current rules, tell the student to verify with the institution's official website or office.
7. Support academic integrity: teach and guide; do not help students deceive teachers.
8. Keep answers focused and reasonably concise.
"""

MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0.4
MAX_TOKENS = 700

# Read the API key from Streamlit Cloud Secrets or local .streamlit/secrets.toml
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.error("Groq API key is missing. Add GROQ_API_KEY in Streamlit app Secrets.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("About EduGuide")
    st.write("An education-focused chatbot powered by Groq.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask an education-related question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        try:
            with st.spinner("EduGuide is thinking..."):
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=api_messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )
                answer = completion.choices[0].message.content or "Sorry, I could not generate a response."
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as exc:
            error_text = str(exc).lower()
            if "authentication" in error_text or "api key" in error_text or "401" in error_text:
                st.error("The Groq API key appears invalid. Check the GROQ_API_KEY secret.")
            elif "rate limit" in error_text or "429" in error_text:
                st.error("The API rate limit was reached. Please wait a little and try again.")
            elif "model" in error_text and ("decommission" in error_text or "not found" in error_text):
                st.error("The configured Groq model may be unavailable. Update MODEL_NAME to a supported model.")
            else:
                st.error("Could not connect to Groq. Check the API key and try again.")
