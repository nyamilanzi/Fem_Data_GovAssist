import streamlit as st
from openai import OpenAI

# Get your API key from Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY")

# Set up the OpenAI client
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Fem_GovAssist Pro", layout="wide")

st.title("Fem_GovAssist Pro: Data Governance Copilot for Malawi")

menu = st.sidebar.selectbox("Choose a tool", ["Legal Q&A", "Consent Form Generator", "Data Sharing Agreement", "Compliance Scorecard"])

if menu == "Legal Q&A":
    st.header("Ask a Data Governance Question")
    query = st.text_area("Enter your question:")
    if st.button("Submit", key="qa_submit"):
        def get_law_context():
            with open("data_protection_malawi.txt", "r") as f:
                return f.read()[:4000]  # keep it under token limit

        context = f"You are an expert on Malawi's Data Protection Act (2024). Refer to the following law excerpt when answering:\n\n{get_law_context()}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query}
            ]
        )
        st.markdown("**Answer:**")
        st.write(response.choices[0].message.content)

elif menu == "Consent Form Generator":
    st.header("Generate a Consent Form")
    population = st.text_input("Target Population")
    data_type = st.text_input("Type of Data Collected")
    purpose = st.text_area("Purpose of Data Collection")
    duration = st.text_input("Duration of Data Use")
    language = st.selectbox("Language", ["English", "Chichewa"])
    if st.button("Generate", key="consent_generate"):
        prompt = f"Create a data collection consent form for participants in {language}. Target group: {population}. Data type: {data_type}. Purpose: {purpose}. Duration: {duration}. Format it as a professional consent document."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compliance officer drafting ethical and legal research consent forms."},
                {"role": "user", "content": prompt}
            ]
        )
        st.markdown("**Generated Consent Form:**")
        st.write(response.choices[0].message.content)

elif menu == "Data Sharing Agreement":
    st.header("Generate a Data Sharing Agreement")
    sender = st.text_input("Data Provider")
    recipient = st.text_input("Data Recipient")
    dataset_desc = st.text_area("Describe the Data")
    use_case = st.text_area("Purpose for Sharing")
    duration = st.text_input("Data Access Duration")
    if st.button("Generate", key="dsa_generate"):
        prompt = f"Draft a Data Sharing Agreement between {sender} and {recipient} regarding the dataset: {dataset_desc}. Purpose: {use_case}. Duration: {duration}. Ensure compliance with Malawi's Data Protection Act."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal assistant specializing in international and national data privacy agreements."},
                {"role": "user", "content": prompt}
            ]
        )
        st.markdown("**Generated Agreement:**")
        st.write(response.choices[0].message.content)

elif menu == "Compliance Scorecard":
    st.header("Data Compliance Self-Assessment")
    st.markdown("Answer the following to assess your data governance risk.")
    consent = st.checkbox("Was informed consent obtained?")
    pii = st.checkbox("Does the dataset contain personally identifiable info?")
    encryption = st.checkbox("Is the data stored with encryption?")
    sharing = st.checkbox("Is the data shared with third parties?")
    if st.button("Score Compliance", key="scorecard"):
        score = 0
        score += 25 if consent else 0
        score += 25 if not pii else 0
        score += 25 if encryption else 0
        score += 25 if not sharing else 0
        st.success(f"Your compliance score is: {score}/100")
        if score < 75:
            st.warning("Review your data practices for better compliance with the Malawi Data Protection Act.")
