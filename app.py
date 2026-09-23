import streamlit as st
from clienthunt_agent import run_clienthunt

st.set_page_config(page_title="ClientHunt AI Agent", page_icon="🎯", layout="centered")

st.title("🎯 AI ClientHunt Agent")
st.write("Find matchable jobs and freelance work across top platforms with tailored workflows.")

# Automatically load Groq API Key from Streamlit Secrets
groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not groq_api_key:
    st.sidebar.header("Configuration")
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

st.header("Search Parameters")

# Exact fields requested
skills = st.text_input("Skills (e.g., Graphic Design, Python, Digital Marketing)")
experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
work_preference = st.text_input("Work Preference (e.g., Remote freelance projects, Part-time)")
location_preference = st.text_input("Location Preference", value="Worldwide remote")
budget_preference = st.text_input("Budget Preference", value="Flexible")
additional_requirements = st.text_area("Additional Requirements")

if st.button("Find your matchable job or work"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud Secrets or the sidebar.")
        st.stop()

    with st.spinner("Searching platforms and generating your matched report... Please wait..."):
        try:
            report_result = run_clienthunt(
                skills=skills,
                experience=experience,
                work_preference=work_preference,
                location_preference=location_preference,
                budget_preference=budget_preference,
                additional_requirements=additional_requirements,
                groq_api_key=groq_api_key,
            )
            
            # Store in session state to persist across reruns
            st.session_state.report = report_result
            
        except Exception as error:
            st.error("Something went wrong while running the agent.")
            st.exception(error)

# Display report if it exists in session state
if "report" in st.session_state:
    if st.session_state.report:
        st.subheader("ClientHunt Matched Report & Workflows")
        st.markdown(st.session_state.report)

        st.download_button(
            label="Download Report (.txt)",
            data=st.session_state.report,
            file_name="clienthunt_matched_report.txt",
            mime="text/plain",
        )
    else:
        st.warning("The agent ran successfully, but returned an empty response. Try broadening your skills or requirements!")
