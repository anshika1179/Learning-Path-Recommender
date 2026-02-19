import streamlit as st
import json
import plotly.express as px
import pandas as pd
from utils_simple import embed_and_store, retrieve_courses
from agents_simple import create_crew
import os

st.set_page_config(page_title="Learning Path Recommender Agent", layout="wide")
st.title("🧠 Learning Path Recommender Agent")

# Initialize DB
if 'collection' not in st.session_state:
    with st.spinner("Loading course catalog and embeddings..."):
        st.session_state.collection = embed_and_store()

# Progress file

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({}, f)

def load_progress():
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

# Sidebar - Onboarding
with st.sidebar:
    st.header("Onboarding")
    skills = st.text_input("Current Skills (comma separated)", "Python basics")
    goals = st.text_area("Learning Goals", "Become a machine learning engineer")
    hours_per_week = st.slider("Hours per week", 1, 30, 10)
    style = st.selectbox("Preferred Style", ["Video", "Reading", "Interactive"])
    if st.button("Generate Roadmap"):
        profile_text = f"Skills: {skills}. Goals: {goals}. Hours/week: {hours_per_week}. Style: {style}."
        st.session_state.profile = profile_text
        st.session_state.progress = load_progress()

# Main area
if 'profile' in st.session_state:
    profile = st.session_state.profile
    progress = st.session_state.progress.get(profile, {"completed": []})
    
    if st.button("🔄 Re-plan with Progress"):
        completed = st.multiselect("Mark completed courses", [c['title'] for c in progress.get("roadmap", [])])
        progress["completed"] = completed
        st.session_state.progress[profile] = progress
        save_progress(st.session_state.progress)
    
    with st.spinner("AI Agents are thinking..."):
        crew = create_crew(profile, " Completed: " + ", ".join(progress.get("completed", [])))
        result = crew.kickoff()
    
    # Simple parsing (in real: use output parser)
    try:
        roadmap = json.loads(result) if isinstance(result, str) else result
    except:
        roadmap = {"roadmap": [{"title": "Sample Course", "week": 1}]}
        st.write("Raw output:", result)
    
    st.success("Personalized Roadmap Generated!")
    
    # Timeline
    df = pd.DataFrame(roadmap.get("roadmap", []))
    if not df.empty and "week" in df.columns:
        fig = px.timeline(df, x_start="week", x_end="week_end", y="title", color="difficulty")
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly Plan
    st.header("Weekly Plan")
    for item in roadmap.get("weekly_plan", []):
        st.write(f"**Week {item['week']}**: {item['tasks']}")
    
    # Chat
    st.header("Chat with your AI Mentor")
    if prompt := st.chat_input("Ask for adjustments, explanations..."):
        st.chat_message("user").write(prompt)
        # Simple response (can expand with another agent)
        st.chat_message("assistant").write(f"Adjusting for: {prompt}. New plan coming soon!")
else:
    st.info("Fill the sidebar to get your personalized learning path!")

st.caption("Built with ❤️ using CrewAI, Streamlit, Chroma & Sentence Transformers")