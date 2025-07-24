import streamlit as st
import pandas as pd

# Sample dummy data
employee_data = {
    "name": "Jane Doe",
    "role": "Software Engineer",
    "skills": ["Python", "Machine Learning", "SQL", "Git"],
    "recommended_courses": [
        {"course": "Advanced Python", "progress": 60},
        {"course": "Deep Learning with TensorFlow", "progress": 30},
        {"course": "Data Engineering on GCP", "progress": 0}
    ],
    "promotion_ready": True
}

team_data = [
    {"name": "Jane Doe", "skills": 4, "promotion_ready": True},
    {"name": "John Smith", "skills": 3, "promotion_ready": False},
    {"name": "Alice Johnson", "skills": 5, "promotion_ready": True},
    {"name": "Bob Lee", "skills": 2, "promotion_ready": False}
]

# Streamlit app
st.set_page_config(page_title="SkillSight Prototype", layout="wide")

st.title("SkillSight – AI-Powered Talent Growth Navigator")

tab1, tab2 = st.tabs(["👩‍💻 Employee Dashboard", "👨‍💼 Manager Dashboard"])

with tab1:
    st.header("Employee Dashboard")
    st.subheader(f"Welcome, {employee_data['name']} ({employee_data['role']})")
    st.markdown("### Current Skills")
    st.write(", ".join(employee_data["skills"]))

    st.markdown("### Recommended Learning Path")
    for course in employee_data["recommended_courses"]:
        st.write(f"**{course['course']}**")
        st.progress(course["progress"])

    st.markdown("### Promotion Readiness")
    if employee_data["promotion_ready"]:
        st.success("🎉 You are ready for promotion!")
    else:
        st.warning("📈 Keep learning to become promotion-ready.")

with tab2:
    st.header("Manager Dashboard")
    st.markdown("### Team Skill Heatmap")
    df = pd.DataFrame(team_data)
    st.dataframe(df.style.background_gradient(cmap='Blues', subset=["skills"]))

    st.markdown("### Promotion Readiness Overview")
    for member in team_data:
        status = "✅ Ready" if member["promotion_ready"] else "❌ Not Ready"
        st.write(f"{member['name']}: {status}")

