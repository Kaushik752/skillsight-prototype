final_code = '''
import streamlit as st
import pandas as pd
import random

# -----------------------------
# Data Generation
# -----------------------------
roles = [
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"
] * 4

skills_pool = ["Python", "SQL", "Communication", "Leadership", "Cloud", "Advanced Python", "Data Visualization"]
industry_standards = {skill: random.randint(6, 9) for skill in skills_pool}

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
    pre_training_scores = {skill: random.randint(4, 8) for skill in skills}
    post_training_scores = {skill: min(pre_training_scores[skill] + random.randint(0, 3), 10) for skill in skills}
    completed_trainings = random.sample(skills, completed)
    pending_trainings = list(set(skills) - set(completed_trainings))
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
        "Post Training Scores": post_training_scores,
        "Completed Trainings": completed_trainings,
        "Pending Trainings": pending_trainings
    })

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("SkillSight Dashboard")

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
    st.markdown(f"**Completed Trainings:** {', '.join(selected_emp['Completed Trainings'])}")
    st.markdown(f"**Pending Trainings:** {', '.join(selected_emp['Pending Trainings'])}")

    st.subheader("Skill Proficiency vs Industry Standards")
    emp_skills = selected_emp["Skills"]
    emp_skill_levels = selected_emp["Post Training Scores"]
    industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}
    comparison_df = pd.DataFrame({
        "Employee": emp_skill_levels,
        "Industry": industry_levels
    })
    st.bar_chart(comparison_df)

    st.subheader("Training Impact")
    pre_scores = selected_emp["Pre Training Scores"]
    post_scores = selected_emp["Post Training Scores"]
    impact_df = pd.DataFrame({
        "Pre-Training": pre_scores,
        "Post-Training": post_scores
    })
    st.line_chart(impact_df)

    st.subheader("Bot Notification")
    if selected_emp["Pending Trainings"]:
        st.info(f"Hi {selected_name}, you have pending trainings: {', '.join(selected_emp['Pending Trainings'])}. Please complete them to stay on track!")
    else:
        st.success(f"Hi {selected_name}, you have completed all your trainings. Great job!")

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
    df["Skill Growth Rate"] = df.apply(lambda row: round(
        sum(row["Post Training Scores"].values()) - sum(row["Pre Training Scores"].values()), 2), axis=1)
    df["Certification Efficiency"] = df["Certifications Completed"] / df["Certifications Enrolled"]
    df_display = df[["Name", "Role", "Experience", "Communication", "Certifications Enrolled",
                     "Certifications Completed", "Promotion Eligible", "Attrition Risk", "Skill Growth Rate", "Certification Efficiency"]]
    st.dataframe(df_display)

    st.subheader("Skill Growth Rate")
    growth_df = df[["Name", "Skill Growth Rate"]].set_index("Name")
    st.bar_chart(growth_df)

    st.subheader("Certification Efficiency")
    cert_df = df[["Name", "Certification Efficiency"]].set_index("Name")
    st.bar_chart(cert_df)

    st.subheader("Team Learning Curve")
    learning_df = pd.DataFrame({
        "Name": df["Name"],
        "Pre-Training Total": df["Pre Training Scores"].apply(lambda x: sum(x.values())),
        "Post-Training Total": df["Post Training Scores"].apply(lambda x: sum(x.values()))
    }).set_index("Name")
    st.line_chart(learning_df)

    st.subheader("Send Notification to Employee")
    emp_name = st.selectbox("Select Employee", df["Name"])
    emp_row = df[df["Name"] == emp_name].iloc[0]
    pending = emp_row["Pending Trainings"]
    default_msg = f"Hi {emp_name}, please complete your pending trainings: {', '.join(pending)}." if pending else f"Hi {emp_name}, great job on completing all trainings!"
    message = st.text_area("Message", value=default_msg)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {emp_name}: {message}")
'''

with open("streamlit_app.py", "w") as f:
    f.write(final_code)

print("Final version of streamlit_app.py has been saved.")



