code = '''
import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data generation
roles = [
    "Software Developer", "Data Analyst", " "Project Manager", "QA Engineer", "DevOps Engineer",
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

# Skill comparison chart using matplotlib
st.subheader("Skill Proficiency vs Industry Standards")
emp_skills = selected_emp["Skills"]
emp_skill_levels = selected_emp["Post Training Scores"]
industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}

fig, ax = plt.subplots()
x = range(len(emp_skills))
ax.bar(x, [emp_skill_levels[skill] for skill in emp_skills], width=0.4, label='Employee', align='center')
ax.bar([i + 0.4 for i in x], [industry_levels[skill] for skill in emp_skills], width=0.4, label='Industry', align='center')
ax.set_xticks([i + 0.2 for i in x])
ax.set_xticklabels(emp_skills)
ax.set_ylabel("Skill Level")
ax.set_title("Skill Comparison")
ax.legend()
st.pyplot(fig)

# Training impact visualization
st.subheader("Training Impact")
pre_scores = selected_emp["Pre Training Scores"]
post_scores = selected_emp["Post Training Scores"]

fig2, ax2 = plt.subplots()
x2 = range(len(emp_skills))
ax2.bar(x2, [pre_scores[skill] for skill in emp_skills], width=0.4, label='Pre-Training', align='center')
ax2.bar([i + 0.4 for i in x2], [post_scores[skill] for skill in emp_skills], width=0.4, label='Post-Training', align='center')
ax2.set_xticks([i + 0.2 for i in x2])
ax2.set_xticklabels(emp_skills)
ax2.set_ylabel("Score")
ax2.set_title("Training Effectiveness")
ax2.legend()
st.pyplot(fig2)

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

# Team skill heatmap
st.subheader("Team Skill Heatmap")
skill_matrix = pd.DataFrame(0, index=[emp["Name"] for emp in employees], columns=skills_pool)
for emp in employees:
    for skill in emp["Skills"]:
        skill_matrix.loc[emp["Name"], skill] = 1

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(skill_matrix, cmap="YlGnBu", cbar=True, ax=ax3)
ax3.set_title("Team Skill Heatmap")
st.pyplot(fig3)
'''

with open("streamlit_app.py", "w") as f:
    f.write(code)

