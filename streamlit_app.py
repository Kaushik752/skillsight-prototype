code = '''
import streamlit as st
import pandas as pd
import random
import numpy as np

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
    pre_training_score = random.randint(50, 80)
    post_training_score = pre_training_score + random.randint(0, 20)
    emp_skill_levels = {skill: random.randint(4, 10) for skill in skills}
    rag_score = completed + (1 if comm_skill == "Advanced" else 0) + (1 if "Excellent" in peer_review or "Strong" in peer_review else 0)
    if rag_score <= 2:
        rag_status = "Red"
    elif rag_score <= 4:
        rag_status = "Amber"
    else:
        rag_status = "Green"
    mentorship_score = experience + (2 if comm_skill == "Advanced" else 1 if comm_skill == "Intermediate" else 0)
    employees.append({
        "Name": f"Employee {i+1}",
        "Role": role,
        "Experience": experience,
        "Skills": skills,
        "Skill Levels": emp_skill_levels,
        "Communication": comm_skill,
        "Peer Review": peer_review,
        "Certifications Enrolled": enrolled,
        "Certifications Completed": completed,
        "Promotion Eligible": promotion,
        "Pre Training Score": pre_training_score,
        "Post Training Score": post_training_score,
        "RAG Status": rag_status,
        "Mentorship Score": mentorship_score
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
    st.markdown(f"**Mentorship Score:** {selected_emp['Mentorship Score']}")
with col2:
    st.markdown(f"**Skills:** {', '.join(selected_emp['Skills'])}")
    st.markdown(f"**Certifications Enrolled:** {selected_emp['Certifications Enrolled']}")
    st.markdown(f"**Certifications Completed:** {selected_emp['Certifications Completed']}")
    st.markdown(f"**Peer Review:** {selected_emp['Peer Review']}")
    st.markdown(f"**RAG Status:** {selected_emp['RAG Status']}")

# Skill comparison chart
st.subheader("Skill Proficiency vs Industry Standards")
emp_skills = selected_emp["Skills"]
emp_skill_levels = selected_emp["Skill Levels"]
industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}
comparison_df = pd.DataFrame({
    "Employee": emp_skill_levels,
    "Industry": industry_levels
})
st.bar_chart(comparison_df)

# SWOT Analysis
st.subheader("SWOT Analysis")
strengths = [skill for skill in emp_skills if emp_skill_levels[skill] > industry_levels[skill]]
weaknesses = [skill for skill in emp_skills if emp_skill_levels[skill] < industry_levels[skill]]
opportunities = [skill for skill in skills_pool if skill not in emp_skills]
threats = [skill for skill in emp_skills if emp_skill_levels[skill] < 6]
st.markdown(f"**Strengths:** {', '.join(strengths)}")
st.markdown(f"**Weaknesses:** {', '.join(weaknesses)}")
st.markdown(f"**Opportunities:** {', '.join(opportunities)}")
st.markdown(f"**Threats:** {', '.join(threats)}")

# Training Effectiveness
st.subheader("Training Effectiveness")
pre = selected_emp["Pre Training Score"]
post = selected_emp["Post Training Score"]
delta = post - pre
st.metric(label="Pre-Training Score", value=pre)
st.metric(label="Post-Training Score", value=post, delta=delta)

# Career Path Suggestions
st.subheader("Career Path Suggestions")
career_paths = {
    "Software Developer": ["Senior Developer", "Tech Lead", "Architect"],
    "Data Analyst": ["Senior Analyst", "Data Scientist", "Analytics Manager"],
    "Project Manager": ["Senior PM", "Program Manager", "Portfolio Manager"],
    "QA Engineer": ["Senior QA", "QA Lead", "Test Architect"],
    "DevOps Engineer": ["Senior DevOps", "DevOps Lead", "Cloud Architect"]
}
suggestions = career_paths.get(selected_emp["Role"], [])
st.markdown(f"**Suggested Path:** {' → '.join([selected_emp['Role']] + suggestions)}")

# Team Overview
st.subheader("Team Overview")
df = pd.DataFrame(employees)
df_display = df.drop(columns=["Skills", "Skill Levels"])
st.dataframe(df_display)

# Team Skill Heatmap
st.subheader("Team Skill Heatmap")
heatmap_data = pd.DataFrame(0, index=[emp["Name"] for emp in employees], columns=skills_pool)
for emp in employees:
    for skill in emp["Skills"]:
        heatmap_data.loc[emp["Name"], skill] = emp["Skill Levels"][skill]
st.dataframe(heatmap_data.style.background_gradient(cmap="YlGnBu"))
'''

with open("streamlit_app.py", "w") as f:
    f.write(code)

