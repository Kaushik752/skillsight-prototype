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
    pre_training_scores = {skill: random.randint(4, 8) for skill in skills}
    post_training_scores = {skill: min(pre_training_scores[skill] + random.randint(0, 3), 10) for skill in skills}
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
        "Pre Training Scores": pre_training_scores,
        "Post Training Scores": post_training_scores
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

# Skill comparison chart using Streamlit native chart
st.subheader("Skill Proficiency vs Industry Standards")
emp_skills = selected_emp["Skills"]
emp_skill_levels = selected_emp["Post Training Scores"]
industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}

comparison_df = pd.DataFrame({
    "Skill": emp_skills,
    "Employee": [emp_skill_levels[skill] for skill in emp_skills],
    "Industry": [industry_levels[skill] for skill in emp_skills]
})
comparison_df.set_index("Skill", inplace=True)
st.bar_chart(comparison_df)

# Training impact visualization using Streamlit native chart
st.subheader("Training Impact")
pre_scores = selected_emp["Pre Training Scores"]
post_scores = selected_emp["Post Training Scores"]

training_df = pd.DataFrame({
    "Skill": emp_skills,
    "Pre-Training": [pre_scores[skill] for skill in emp_skills],
    "Post-Training": [post_scores[skill] for skill in emp_skills]
})
training_df.set_index("Skill", inplace=True)
st.line_chart(training_df)

# Team overview with RAG analysis
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
df_display = df.drop(columns=["Skills", "Peer Review", "Pre Training Scores", "Post Training Scores"])
st.dataframe(df_display)

# Team skill heatmap using Streamlit native chart
st.subheader("Team Skill Distribution")
skill_counts = {skill: 0 for skill in skills_pool}
for emp in employees:
    for skill in emp["Skills"]:
        skill_counts[skill] += 1
skill_df = pd.DataFrame.from_dict(skill_counts, orient='index', columns=['Count'])
st.bar_chart(skill_df)

