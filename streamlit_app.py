import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="SkillSight Dashboard", layout="wide")

# Title
st.title("📊 SkillSight – AI-Powered Talent Growth Navigator")

# Generate dummy data
roles = ["Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"]
skills_pool = ["Python", "SQL", "Project Management", "Testing", "CI/CD", "Advanced Python", "Communication", "Leadership"]
industry_standards = {
    "Python": 8,
    "SQL": 7,
    "Project Management": 7,
    "Testing": 6,
    "CI/CD": 7,
    "Advanced Python": 8,
    "Communication": 8,
    "Leadership": 7
}

num_employees = 20
employees = []

for i in range(num_employees):
    role = random.choice(roles)
    experience = random.randint(1, 10)
    skills = random.sample(skills_pool, k=random.randint(3, 5))
    peer_review = random.choice([
        "Excellent team player", "Strong technical skills", "Needs improvement in communication",
        "Great leadership potential", "Consistently meets deadlines"
    ])
    communication = random.choice(["Excellent", "Good", "Average", "Needs Improvement"])
    enrolled = random.randint(1, 5)
    completed = random.randint(0, enrolled)
    promotion_eligible = "Yes" if random.random() < 0.25 else "No"

    employees.append({
        "Name": f"Employee {i+1}",
        "Role": role,
        "Experience (Years)": experience,
        "Skills": skills,
        "Peer Review": peer_review,
        "Communication Skills": communication,
        "Certifications Enrolled": enrolled,
        "Certifications Completed": completed,
        "Promotion Eligible": promotion_eligible
    })

# Sidebar for employee selection
st.sidebar.header("🔍 Select Employee")
selected_name = st.sidebar.selectbox("Choose an employee", [emp["Name"] for emp in employees])

# Get selected employee data
selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

# Display employee profile
st.subheader(f"👤 Profile: {selected_name}")
col1, col2, col3 = st.columns(3)
col1.metric("Role", selected_emp["Role"])
col2.metric("Experience", f"{selected_emp['Experience (Years)']} years")
col3.metric("Promotion Eligible", selected_emp["Promotion Eligible"])

col4, col5 = st.columns(2)
col4.metric("Communication Skills", selected_emp["Communication Skills"])
col5.metric("Peer Review", selected_emp["Peer Review"])

st.markdown("### 🧠 Skills")
st.write(", ".join(selected_emp["Skills"]))

st.markdown("### 🎓 Certifications")
st.progress(selected_emp["Certifications Completed"] / selected_emp["Certifications Enrolled"] if selected_emp["Certifications Enrolled"] > 0 else 0)

# Skill comparison chart
st.markdown("### 📈 Skill Proficiency vs Industry Standards")
emp_skill_levels = {skill: random.randint(5, 9) for skill in selected_emp["Skills"]}
skills = list(emp_skill_levels.keys())
emp_levels = [emp_skill_levels[skill] for skill in skills]
industry_levels = [industry_standards.get(skill, 7) for skill in skills]

fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(skills))
width = 0.35
ax.bar(x - width/2, emp_levels, width, label='Employee')
ax.bar(x + width/2, industry_levels, width, label='Industry')
ax.set_ylabel('Proficiency Level (1-10)')
ax.set_title('Skill Comparison')
ax.set_xticks(x)
ax.set_xticklabels(skills, rotation=45)
ax.legend()
st.pyplot(fig)

# Team overview
st.markdown("### 👥 Team Overview")
df = pd.DataFrame(employees)
df["Skills"] = df["Skills"].apply(lambda x: ", ".join(x))
st.dataframe(df.drop(columns=["Peer Review"]), use_container_width=True)

