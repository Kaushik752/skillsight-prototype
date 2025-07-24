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

# Generate employee data
employees = []
for i in range(20):
    role = roles[i]
    skills = random.sample(skills_pool, 4)
    experience = random.randint(1, 10)
    comm_skill = random.choice(["Beginner", "Intermediate", "Advanced"])
    peer_review = random.choice(["Excellent team player", "Strong communicator", "Needs improvement", "Technically sound"])
    enrolled = random.randint(1, 4)
    trainings = random.sample(skills, min(enrolled, len(skills)))
    completed = random.randint(0, len(trainings))
    completed_trainings = random.sample(trainings, completed)
    pending_trainings = list(set(trainings) - set(completed_trainings))
    promotion = "Yes" if i < 5 else "No"
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
        "Pending Trainings": [training_catalog[skill] for skill in pending_trainings]
    })

# Streamlit UI
st.set_page_config(layout="wide")
st.title("SkillSight Dashboard")

# View toggle
view_mode = st.sidebar.radio("Select View", ["Employee View", "Manager View"])

if view_mode == "Employee View":
    selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

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

    st.subheader("Training Summary")
    st.markdown("**✅ Completed Trainings:**")
    st.write(selected_emp["Completed Trainings"])
    st.markdown("**⏳ Pending Trainings:**")
    st.write(selected_emp["Pending Trainings"])

    st.subheader("Bot Notification")
    if selected_emp["Pending Trainings"]:
        st.info(f"Hi {selected_name}, you have {len(selected_emp['Pending Trainings'])} pending trainings. Please complete: {', '.join(selected_emp['Pending Trainings'])}")
    else:
        st.success("You have completed all your trainings. Great job!")

elif view_mode == "Manager View":
    st.subheader("Team Overview")
    df = pd.DataFrame(employees)
    df_display = df[["Name", "Role", "Experience", "Communication", "Certifications Enrolled", "Certifications Completed", "Promotion Eligible"]]
    st.dataframe(df_display)

    st.subheader("Send Notification to Employee")
    selected_name = st.selectbox("Select Employee to Notify", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)
    if selected_emp["Pending Trainings"]:
        message = f"Dear {selected_name}, please complete the following trainings: {', '.join(selected_emp['Pending Trainings'])}"
    else:
        message = f"Dear {selected_name}, you have completed all your trainings. Keep up the good work!"

    st.text_area("Notification Message", value=message, height=100)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {selected_name}")

