code = '''
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
industry_standards = {skill: random.randint(6, 9) for skill in skills_pool}

# Generate 20 employees
employees = []
for i in range(20):
    role = roles[i]
    skills = random.sample(skills_pool, 4)
    experience = random.randint(1, 10)
    comm_skill = random.choice(["Beginner", "Intermediate", "Advanced"])
    peer_review = random.choice(["Excellent team player", "Strong communicator", "Needs improvement", "Technically sound"])
    enrolled = random.randint(1, 5)
    completed = random.randint(0, enrolled)
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
        "Promotion Eligible": promotion
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

# Skill comparison chart
st.subheader("Skill Proficiency vs Industry Standards")
emp_skills = selected_emp["Skills"]
emp_skill_levels = {skill: random.randint(4, 10) for skill in emp_skills}
industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}

comparison_df = pd.DataFrame({
    "Employee": emp_skill_levels,
    "Industry": industry_levels
})

st.bar_chart(comparison_df)

# Team overview
st.subheader("Team Overview")
df = pd.DataFrame(employees)
df_display = df.drop(columns=["Skills", "Peer Review"])
st.dataframe(df_display)
'''

# Save to file
with open("streamlit_app.py", "w") as f:
    f.write(code)

