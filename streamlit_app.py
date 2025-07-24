import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# Set up Streamlit page
st.set_page_config(layout="wide")
st.title("SkillSight: Team Performance & Learning Analytics")

# Define skills and roles
skills_pool = ["Python", "SQL", "Communication", "Leadership", "Cloud", "Advanced Python", "Data Visualization"]
roles = ["Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"] * 4

# Generate synthetic employee data
employees = []
for i in range(20):
    name = f"Employee {i+1}"
    role = roles[i]
    skills = random.sample(skills_pool, 4)
    experience = random.randint(1, 10)
    comm_skill = random.choice(["Beginner", "Intermediate", "Advanced"])
    peer_review = random.choice(["Excellent", "Good", "Average", "Needs Improvement"])
    enrolled = random.randint(1, len(skills))
    completed = random.randint(0, enrolled)
    pre_scores = {skill: random.randint(4, 7) for skill in skills}
    post_scores = {skill: min(pre_scores[skill] + random.randint(0, 3), 10) for skill in skills}
    skill_growth = round(sum(post_scores[skill] - pre_scores[skill] for skill in skills) / len(skills), 2)
    cert_efficiency = round(completed / enrolled, 2) if enrolled > 0 else 0
    learning_curve = [pre_scores[skill] for skill in skills] + [post_scores[skill] for skill in skills]
    employees.append({
        "Name": name,
        "Role": role,
        "Experience": experience,
        "Skills": skills,
        "Communication": comm_skill,
        "Peer Review": peer_review,
        "Certifications Enrolled": enrolled,
        "Certifications Completed": completed,
        "Pre Training Scores": pre_scores,
        "Post Training Scores": post_scores,
        "Skill Growth Rate": skill_growth,
        "Certification Efficiency": cert_efficiency,
        "Learning Curve": learning_curve
    })

# Convert to DataFrame
df = pd.DataFrame(employees)

# Display team overview
st.subheader("Team Overview")
overview_df = df[["Name", "Role", "Experience", "Communication", "Peer Review", "Certifications Enrolled", "Certifications Completed", "Skill Growth Rate", "Certification Efficiency"]]
st.dataframe(overview_df)

# Plot average skill growth
st.subheader("Average Skill Growth Rate")
fig1, ax1 = plt.subplots()
sns.barplot(data=overview_df, x="Name", y="Skill Growth Rate", ax=ax1)
ax1.set_xticklabels(overview_df["Name"], rotation=45, ha='right')
st.pyplot(fig1)

# Plot certification efficiency
st.subheader("Certification Completion Efficiency")
fig2, ax2 = plt.subplots()
sns.barplot(data=overview_df, x="Name", y="Certification Efficiency", ax=ax2)
ax2.set_xticklabels(overview_df["Name"], rotation=45, ha='right')
st.pyplot(fig2)

# Plot learning curves
st.subheader("Learning Curve Trends")
fig3, ax3 = plt.subplots(figsize=(10, 6))
for emp in employees:
    ax3.plot(emp["Learning Curve"], label=emp["Name"])
ax3.set_title("Learning Curves (Pre & Post Training Scores)")
ax3.set_xlabel("Skill Index")
ax3.set_ylabel("Score")
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
st.pyplot(fig3)

