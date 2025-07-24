import streamlit as st
import pandas as pd
import random
from PIL import Image

# Load and display logo
st.set_page_config(layout="wide")
logo_path = "skillsight_logo.png"
try:
    logo = Image.open(logo_path)
    st.image(logo, width=100)
except:
    st.warning("Logo image not found. Please upload 'skillsight_logo.png'.")

st.title("SkillSight Dashboard")
st.markdown("**Powered by Innovaccer-GE-OPs Team**")

# View toggle
view_mode = st.sidebar.radio("Select View Mode", ["Employee View", "Manager View"])

# Sample data generation
roles = [
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"
]
skills_pool = ["Python", "SQL", "Communication", "Leadership", "Cloud", "Advanced Python", "Data Visualization"]
training_catalog = {
    "Python": "Python for Beginners",
    "SQL": "Mastering SQL",
    "Communication": "Effective Communication",
    "Leadership": "Leadership Essentials",
    "Cloud": "Cloud Fundamentals",
    "Advanced Python": "Advanced Python Programming",
    "Data Visualization": "Data Visualization with Python"
}
industry_standards = {skill: random.randint(6, 9) for skill in skills_pool}

# Generate employees
employees = []
for i in range(20):
    role = roles[i]
    skills = random.sample(skills_pool, 4)
    experience = random.randint(1, 10)
    comm_skill = random.choice(["Beginner", "Intermediate", "Advanced"])
    peer_review = random.choice(["Excellent team player", "Strong communicator", "Needs improvement", "Technically sound"])
    enrolled = random.randint(1, len(skills))
    completed = random.randint(0, enrolled)
    promotion = "Yes" if i < 5 else "No"
    pre_scores = {skill: random.randint(4, 8) for skill in skills}
    post_scores = {skill: min(pre_scores[skill] + random.randint(0, 3), 10) for skill in skills}
    completed_trainings = random.sample(skills, completed)
    pending_trainings = [s for s in skills if s not in completed_trainings]
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
        "Pre Training Scores": pre_scores,
        "Post Training Scores": post_scores,
        "Completed Trainings": [training_catalog[s] for s in completed_trainings],
        "Pending Trainings": [training_catalog[s] for s in pending_trainings]
    })

# Sidebar employee selection
selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

# Employee View
if view_mode == "Employee View":
    st.subheader(f"Profile: {selected_name}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Role:** {selected_emp['Role']}")
        st.markdown(f"**Experience:** {selected_emp['Experience']} years")
        st.markdown(f"**Communication Skills:** {selected_emp['Communication']}")
    with col2:
        st.markdown(f"**Skills:** {', '.join(selected_emp['Skills'])}")
        st.markdown(f"**Certifications Enrolled:** {selected_emp['Certifications Enrolled']}")
        st.markdown(f"**Certifications Completed:** {selected_emp['Certifications Completed']}")

    st.subheader("Training Summary")
    st.markdown("**Completed Trainings:**")
    st.write(selected_emp["Completed Trainings"])
    st.markdown("**Pending Trainings:**")
    st.write(selected_emp["Pending Trainings"])

    st.subheader("Skill Proficiency vs Industry Standards")
    skill_df = pd.DataFrame({
        "Skill": selected_emp["Skills"],
        "Employee": [selected_emp["Post Training Scores"][s] for s in selected_emp["Skills"]],
        "Industry": [industry_standards[s] for s in selected_emp["Skills"]]
    }).set_index("Skill")
    st.bar_chart(skill_df)

    st.subheader("Training Impact")
    impact_df = pd.DataFrame({
        "Skill": selected_emp["Skills"],
        "Pre-Training": [selected_emp["Pre Training Scores"][s] for s in selected_emp["Skills"]],
        "Post-Training": [selected_emp["Post Training Scores"][s] for s in selected_emp["Skills"]]
    }).set_index("Skill")
    st.line_chart(impact_df)

    st.subheader("Bot Notification")
    if selected_emp["Pending Trainings"]:
        st.info(f"Hi {selected_name}, you have pending trainings: {', '.join(selected_emp['Pending Trainings'])}. Please complete them to stay on track!")

# Manager View
else:
    st.subheader("Team Overview")
    df = pd.DataFrame(employees)
    def rag_status(row):
        if row["Certifications Completed"] < row["Certifications Enrolled"] / 2 and row["Communication"] == "Beginner":
            return "Red"
        elif row["Certifications Completed"] < row["Certifications Enrolled"]:
            return "Amber"
        else:
            return "Green"
    df["Attrition Risk"] = df.apply(rag_status, axis=1)
    df_display = df[["Name", "Role", "Experience", "Communication", "Certifications Enrolled", "Certifications Completed", "Promotion Eligible", "Peer Review", "Attrition Risk"]]
    st.dataframe(df_display)

    st.subheader("Skill Growth Rate")
    growth_data = []
    for emp in employees:
        pre = sum(emp["Pre Training Scores"].values())
        post = sum(emp["Post Training Scores"].values())
        growth = round((post - pre) / len(emp["Skills"]), 2)
        growth_data.append({"Name": emp["Name"], "Skill Growth Rate": growth})
    growth_df = pd.DataFrame(growth_data).set_index("Name")
    st.bar_chart(growth_df)

    st.subheader("Certification Summary")
    cert_data = [{"Name": emp["Name"], "Completed Trainings": ", ".join(emp["Completed Trainings"]), "Pending Trainings": ", ".join(emp["Pending Trainings"])} for emp in employees]
    cert_df = pd.DataFrame(cert_data)
    st.dataframe(cert_df)

    st.subheader("Send Notification to Employee")
    notify_name = st.selectbox("Select Employee to Notify", [emp["Name"] for emp in employees])
    notify_emp = next(emp for emp in employees if emp["Name"] == notify_name)
    default_msg = f"Hi {notify_name}, please complete your pending trainings: {', '.join(notify_emp['Pending Trainings'])}."
    message = st.text_area("Notification Message", value=default_msg)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {notify_name}!")

