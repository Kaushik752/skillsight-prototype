import streamlit as st
import pandas as pd
import random
import datetime

# Set page config
st.set_page_config(layout="wide", page_title="SkillSight Dashboard")

# Title and logo
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("skillsight_logo.png", width=80)
with col_title:
    st.title("SkillSight Dashboard")
    st.caption("Powered by Innovaccer-GE-OPs Team")

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
        "Completed Trainings": completed_trainings,
        "Pending Trainings": pending_trainings,
        "Promotion Eligible": promotion,
        "Pre Training Scores": pre_training_scores,
        "Post Training Scores": post_training_scores
    })

# View toggle
view_mode = st.sidebar.radio("Select View Mode", ["Employee View", "Manager View"])

if view_mode == "Employee View":
    selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

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
        st.markdown(f"**Completed Trainings:** {', '.join(selected_emp['Completed Trainings'])}")
        st.markdown(f"**Pending Trainings:** {', '.join(selected_emp['Pending Trainings'])}")

    # Skill comparison
    st.subheader("Skill Proficiency vs Industry Standards")
    emp_skills = selected_emp["Skills"]
    emp_skill_levels = selected_emp["Post Training Scores"]
    industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}
    comparison_df = pd.DataFrame({
        "Employee": emp_skill_levels,
        "Industry": industry_levels
    })
    st.bar_chart(comparison_df)

    # Training impact
    st.subheader("Training Impact")
    training_df = pd.DataFrame({
        "Pre-Training": selected_emp["Pre Training Scores"],
        "Post-Training": selected_emp["Post Training Scores"]
    })
    st.line_chart(training_df)

    # Bot notification
    st.subheader("SkillSight Bot")
    if selected_emp["Pending Trainings"]:
        st.info(f"Hi {selected_name}, you have pending trainings: {', '.join(selected_emp['Pending Trainings'])}. Please complete them to enhance your skills.")
    else:
        st.success(f"Hi {selected_name}, you have completed all your trainings. Great job!")

else:
    st.subheader("Manager View")

    df = pd.DataFrame(employees)

    # Attrition Risk
    def rag_status(row):
        if row["Certifications Completed"] < row["Certifications Enrolled"] / 2 and row["Communication"] == "Beginner":
            return "Red"
        elif row["Certifications Completed"] < row["Certifications Enrolled"]:
            return "Amber"
        else:
            return "Green"
    df["Attrition Risk"] = df.apply(rag_status, axis=1)

    # Skill Growth Rate
    def skill_growth(row):
        pre = row["Pre Training Scores"]
        post = row["Post Training Scores"]
        return round(sum(post[s] - pre[s] for s in pre) / len(pre), 2)
    df["Skill Growth Rate"] = df.apply(skill_growth, axis=1)

    # Certification Efficiency
    df["Certification Efficiency"] = df["Certifications Completed"] / df["Certifications Enrolled"]

    # Role Readiness Score
    def readiness(row):
        score = 0
        score += row["Experience"] * 0.2
        score += row["Certification Efficiency"] * 5
        score += 1 if row["Communication"] == "Advanced" else 0.5 if row["Communication"] == "Intermediate" else 0
        return round(score, 2)
    df["Role Readiness Score"] = df.apply(readiness, axis=1)

    # Mentorship Potential
    df["Mentorship Potential"] = df.apply(lambda r: "High" if r["Experience"] >= 7 and r["Communication"] == "Advanced" else "Moderate" if r["Experience"] >= 5 else "Low", axis=1)

    # Succession Planning
    df["Successor Potential"] = df["Role Readiness Score"].apply(lambda x: "Yes" if x > 3.5 else "No")

    # Team Overview
    st.markdown("### Team Overview")
    display_cols = ["Name", "Role", "Experience", "Communication", "Peer Review", "Certifications Enrolled", "Certifications Completed", "Completed Trainings", "Pending Trainings", "Attrition Risk", "Skill Growth Rate", "Certification Efficiency", "Role Readiness Score", "Mentorship Potential", "Successor Potential"]
    st.dataframe(df[display_cols])

    # Skill Growth Rate Chart
    st.markdown("### Skill Growth Rate Across Team")
    growth_df = df[["Name", "Skill Growth Rate"]].set_index("Name")
    st.bar_chart(growth_df)

    # Certification Efficiency Chart
    st.markdown("### Certification Efficiency")
    cert_df = df[["Name", "Certification Efficiency"]].set_index("Name")
    st.bar_chart(cert_df)

    # Learning Curve
    st.markdown("### Team Learning Curve (Average Pre vs Post Training Scores)")
    learning_data = []
    for emp in employees:
        avg_pre = sum(emp["Pre Training Scores"].values()) / len(emp["Pre Training Scores"])
        avg_post = sum(emp["Post Training Scores"].values()) / len(emp["Post Training Scores"])
        learning_data.append({"Name": emp["Name"], "Pre": avg_pre, "Post": avg_post})
    learning_df = pd.DataFrame(learning_data).set_index("Name")
    st.line_chart(learning_df)

    # Skill Distribution Pareto Chart
    st.markdown("### Skill Distribution (Pareto Analysis)")
    skill_counts = {}
    for emp in employees:
        for skill in emp["Skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    skill_df = pd.DataFrame.from_dict(skill_counts, orient='index', columns=["Count"]).sort_values(by="Count", ascending=False)
    skill_df["Cumulative %"] = skill_df["Count"].cumsum() / skill_df["Count"].sum() * 100
    st.bar_chart(skill_df[["Count"]])

    # Notification System
    st.markdown("### Notify Employee")
    emp_to_notify = st.selectbox("Select Employee", df["Name"])
    pending = df[df["Name"] == emp_to_notify]["Pending Trainings"].values[0]
    if pending:
        default_msg = f"Hi {emp_to_notify}, please complete your pending trainings: {', '.join(pending)}."
    else:
        default_msg = f"Hi {emp_to_notify}, you have completed all trainings. Great job!"
    msg = st.text_area("Message", value=default_msg)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {emp_to_notify}!")

