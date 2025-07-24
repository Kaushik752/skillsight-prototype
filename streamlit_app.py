import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
import plotly.express as px

# Set page config with dark theme
st.set_page_config(page_title="SkillSight 2050", layout="wide")

# Apply custom CSS for futuristic look
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background-color: #0f1117;
    }
    .css-1d391kg {
        background-color: #1c1e26;
        border-radius: 10px;
        padding: 20px;
    }
    .css-1v0mbdj {
        color: #00ffe7;
    }
    </style>
""", unsafe_allow_html=True)

# Sample data generation
roles = [
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"
] * 4
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

# Sidebar for employee selection
st.sidebar.title("SkillSight 2050")
selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

# Employee profile
st.title(f"👤 Profile: {selected_name}")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**🧑 Role:** {selected_emp['Role']}")
    st.markdown(f"**📅 Experience:** {selected_emp['Experience']} years")
    st.markdown(f"**🗣️ Communication Skills:** {selected_emp['Communication']}")
    st.markdown(f"**🚀 Promotion Eligible:** {selected_emp['Promotion Eligible']}")
with col2:
    st.markdown(f"**🧠 Skills:** {', '.join(selected_emp['Skills'])}")
    st.markdown(f"**📚 Certifications Enrolled:** {selected_emp['Certifications Enrolled']}")
    st.markdown(f"**✅ Certifications Completed:** {selected_emp['Certifications Completed']}")
    st.markdown(f"**🧾 Peer Review:** {selected_emp['Peer Review']}")

# Skill comparison chart using Plotly
st.subheader("📊 Skill Proficiency vs Industry Standards")
emp_skills = selected_emp["Skills"]
emp_skill_levels = selected_emp["Post Training Scores"]
industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}

comparison_df = pd.DataFrame({
    "Skill": emp_skills,
    "Employee": [emp_skill_levels[skill] for skill in emp_skills],
    "Industry": [industry_levels[skill] for skill in emp_skills]
})

fig = go.Figure()
fig.add_trace(go.Bar(x=comparison_df["Skill"], y=comparison_df["Employee"], name='Employee', marker_color='cyan'))
fig.add_trace(go.Bar(x=comparison_df["Skill"], y=comparison_df["Industry"], name='Industry', marker_color='magenta'))
fig.update_layout(barmode='group', template='plotly_dark', title="Skill Comparison")
st.plotly_chart(fig, use_container_width=True)

# Training impact visualization
st.subheader("📈 Training Impact")
pre_scores = selected_emp["Pre Training Scores"]
post_scores = selected_emp["Post Training Scores"]

training_df = pd.DataFrame({
    "Skill": emp_skills,
    "Pre-Training": [pre_scores[skill] for skill in emp_skills],
    "Post-Training": [post_scores[skill] for skill in emp_skills]
})

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=training_df["Skill"], y=training_df["Pre-Training"], mode='lines+markers', name='Pre-Training', line=dict(color='orange')))
fig2.add_trace(go.Scatter(x=training_df["Skill"], y=training_df["Post-Training"], mode='lines+markers', name='Post-Training', line=dict(color='lime')))
fig2.update_layout(template='plotly_dark', title="Training Effectiveness")
st.plotly_chart(fig2, use_container_width=True)

# Team overview with RAG analysis
st.subheader("🧑‍🤝‍🧑 Team Overview")
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

# Team skill heatmap using Plotly
st.subheader("🌐 Team Skill Heatmap")
skill_matrix = pd.DataFrame(0, index=[emp["Name"] for emp in employees], columns=skills_pool)
for emp in employees:
    for skill in emp["Skills"]:
        skill_matrix.loc[emp["Name"], skill] = 1

heatmap_fig = px.imshow(skill_matrix, color_continuous_scale='Viridis', aspect='auto', title="Skill Distribution Across Team")
heatmap_fig.update_layout(template='plotly_dark')
st.plotly_chart(heatmap_fig, use_container_width=True)

