import streamlit as st
import pandas as pd
import random

# Sample data generation
roles = [
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"
]
skills_pool = ["Python", "SQL", "Communication", "Leadership", "Cloud", "Advanced Python", "Data Visualization"]
training_catalog = {
    "Python": "Python for Developers",
    "SQL": "Advanced SQL Queries",
    "Communication": "Effective Communication",
    "Leadership": "Leadership Essentials",
    "Cloud": "Cloud Fundamentals",
    "Advanced Python": "Mastering Python",
    "Data Visualization": "Data Viz with Python"
}
industry_standards = {skill: random.randint(6, 9) for skill in skills_pool}

# Generate 20 employees
employees = []
for i in range(20):
    role = roles[i]
    skills = random.sample(skills_pool, 4)
    experience = random.randint(1, 10)
    comm_skill = random.choice(["Beginner", "Intermediate", "Advanced"])
    peer_review = random.choice(["Excellent team player", "Strong communicator", "Needs improvement", "Technically sound"])
    enrolled = random.randint(1, len(skills))  # Ensure enrolled does not exceed number of skills
    completed = random.randint(0, enrolled)
    promotion = "Yes" if i < 5 else "No"
    trainings = random.sample(skills, enrolled)
    completed_trainings = trainings[:completed]
    pending_trainings = trainings[completed:]
    employees.append({
        "Name": f"Employee {i+1}",
        "Role": role,
        "Experience": experience,
        "Skills": skills,
        "Communication": comm_skill,
        "Peer Review": peer_review,
        "Certifications Enrolled": enrolled,
        "Certifications Completed": completed,
        "Promotion Eligible": promotion,
        "Completed Trainings": [training_catalog[skill] for skill in completed_trainings],
        "Pending Trainings": [training_catalog[skill] for skill in pending_trainings],
        "Learning Path": [training_catalog[skill] for skill in skills if skill not in completed_trainings]
    })

# Streamlit UI
st.set_page_config(layout="wide")
st.title("SkillSight Dashboard")

# Sidebar for employee selection
selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

# Employee profile
st.subheader(f"Profile: {selected_name}")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Role:** {selected_emp['Role']}")
    st.markdown(f"**Experience:** {selected_emp['Experience']} years")
    st.markdown(f"**Communication Skills:** {selected_emp['Communication']}")
    st.markdown(f"**Promotion Eligible:** {selected_emp['Promotion Eligible']}")
with col2:
    st.markdown(f"**Skills:** {', '.join(selected_emp['Skills'])}")
    st.markdown(f"**Certifications Enrolled:** {selected_emp['Certifications Enrolled']}")
    st.markdown(f"**Certifications Completed:** {selected_emp['Certifications Completed']}")
    st.markdown(f"**Peer Review:** {selected_emp['Peer Review']}")

# Chatbot-like notification panel
st.subheader("📢 Training Bot Notification")
with st.expander("View Training Notifications"):
    st.markdown(f"👋 Hello **{selected_name}**, here's your training update:")
    st.markdown(f"- ✅ You have completed **{selected_emp['Certifications Completed']}** out of **{selected_emp['Certifications Enrolled']}** trainings.")
    if selected_emp["Pending Trainings"]:
        st.markdown(f"- ⏳ Pending Trainings: {', '.join(selected_emp['Pending Trainings'])}")
    else:
        st.markdown("- 🎉 All trainings completed!")
    if selected_emp["Learning Path"]:
        st.markdown(f"- 📚 Recommended Learning Path: {', '.join(selected_emp['Learning Path'])}")
    else:
        st.markdown("- 🚀 You're up to date with your learning path!")

# Training details
st.subheader("📘 Training Summary")
col3, col4 = st.columns(2)
with col3:
    st.markdown("### ✅ Completed Trainings")
    if selected_emp["Completed Trainings"]:
        for t in selected_emp["Completed Trainings"]:
            st.markdown(f"- {t}")
    else:
        st.markdown("No trainings completed yet.")
with col4:
    st.markdown("### ⏳ Pending Trainings")
    if selected_emp["Pending Trainings"]:
        for t in selected_emp["Pending Trainings"]:
            st.markdown(f"- {t}")
    else:
        st.markdown("No pending trainings.")



