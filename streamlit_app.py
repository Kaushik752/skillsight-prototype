import streamlit as st
import pandas as pd
import random

# Set page config and logo
st.set_page_config(layout="wide", page_title="SkillSight Dashboard")
st.image("skillsight_logo.png", width=120)
st.markdown("### SkillSight Dashboard")
st.markdown("#### Powered by Innovaccer-GE-OPs Team")

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

    st.markdown("**Completed Trainings:**")
    st.write(selected_emp["Completed Trainings"])
    st.markdown("**Pending Trainings:**")
    st.write(selected_emp["Pending Trainings"])

    st.subheader("Training Impact")
    training_df = pd.DataFrame({
        "Skill": selected_emp["Skills"],
        "Pre-Training": [selected_emp["Pre Training Scores"][s] for s in selected_emp["Skills"]],
        "Post-Training": [selected_emp["Post Training Scores"][s] for s in selected_emp["Skills"]]
    })
    st.line_chart(training_df.set_index("Skill"))

    st.subheader("Skill Proficiency vs Industry Standards")
    comparison_df = pd.DataFrame({
        "Skill": selected_emp["Skills"],
        "Employee": [selected_emp["Post Training Scores"][s] for s in selected_emp["Skills"]],
        "Industry": [industry_standards[s] for s in selected_emp["Skills"]]
    })
    st.bar_chart(comparison_df.set_index("Skill"))

else:
    st.subheader("Team Overview")
    df = pd.DataFrame(employees)
    df["Attrition Risk"] = df.apply(
        lambda row: "Red" if row["Certifications Completed"] < row["Certifications Enrolled"] / 2 and row["Communication"] == "Beginner"
        else "Amber" if row["Certifications Completed"] < row["Certifications Enrolled"]
        else "Green", axis=1)
    df_display = df[["Name", "Role", "Experience", "Communication", "Certifications Enrolled", "Certifications Completed", "Promotion Eligible", "Peer Review", "Attrition Risk"]]
    st.dataframe(df_display)

    st.subheader("Skill Growth Rate")
    df["Skill Growth Rate"] = df.apply(lambda row: round(
        sum(row["Post Training Scores"][s] - row["Pre Training Scores"][s] for s in row["Skills"]) / len(row["Skills"]), 2), axis=1)
    growth_df = df[["Name", "Skill Growth Rate"]].set_index("Name")
    st.bar_chart(growth_df)

    st.subheader("Certification Summary")
    for emp in employees:
        st.markdown(f"**{emp['Name']}**")
        st.markdown(f"Completed Trainings: {', '.join(emp['Completed Trainings'])}")
        st.markdown(f"Pending Trainings: {', '.join(emp['Pending Trainings'])}")
        st.markdown("---")

    st.subheader("Send Notification to Employee")
    selected_name = st.selectbox("Select Employee to Notify", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)
    default_message = f"Hi {selected_name}, please complete your pending trainings: {', '.join(selected_emp['Pending Trainings'])}."
    message = st.text_area("Notification Message", value=default_message)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {selected_name}!")


