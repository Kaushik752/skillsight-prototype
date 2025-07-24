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
    max_trainings = len(skills)
    enrolled = random.randint(1, max_trainings)
    completed = random.randint(0, enrolled)
    trainings = random.sample(skills, enrolled)
    completed_trainings = random.sample(trainings, completed)
    pending_trainings = list(set(trainings) - set(completed_trainings))
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
        "Post Training Scores": post_training_scores,
        "Trainings Assigned": trainings,
        "Trainings Completed": completed_trainings,
        "Trainings Pending": pending_trainings
    })

# Streamlit UI
st.set_page_config(layout="wide")
st.title("SkillSight Dashboard")

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
        st.markdown(f"**Promotion Eligible:** {selected_emp['Promotion Eligible']}")
    with col2:
        st.markdown(f"**Skills:** {', '.join(selected_emp['Skills'])}")
        st.markdown(f"**Certifications Enrolled:** {selected_emp['Certifications Enrolled']}")
        st.markdown(f"**Certifications Completed:** {selected_emp['Certifications Completed']}")
        st.markdown(f"**Peer Review:** {selected_emp['Peer Review']}")

    st.subheader("Training Summary")
    st.markdown(f"**Trainings Completed:** {', '.join(selected_emp['Trainings Completed'])}")
    st.markdown(f"**Trainings Pending:** {', '.join(selected_emp['Trainings Pending'])}")

    st.subheader("Bot Notification")
    st.info(f"Hi {selected_name}, you have {len(selected_emp['Trainings Pending'])} pending trainings: {', '.join(selected_emp['Trainings Pending'])}. Please complete them to stay on track with your learning path.")

    st.subheader("Training Impact")
    emp_skills = selected_emp["Skills"]
    pre_scores = selected_emp["Pre Training Scores"]
    post_scores = selected_emp["Post Training Scores"]
    training_df = pd.DataFrame({
        "Pre-Training": [pre_scores[skill] for skill in emp_skills],
        "Post-Training": [post_scores[skill] for skill in emp_skills]
    }, index=emp_skills)
    st.line_chart(training_df)

    st.subheader("Skill Proficiency vs Industry Standards")
    industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}
    comparison_df = pd.DataFrame({
        "Employee": [post_scores[skill] for skill in emp_skills],
        "Industry": [industry_levels[skill] for skill in emp_skills]
    }, index=emp_skills)
    st.bar_chart(comparison_df)

else:
    st.subheader("Manager View: Team Overview")
    df = pd.DataFrame(employees)
    def rag_status(row):
        if row["Certifications Completed"] < row["Certifications Enrolled"] / 2 and row["Communication"] == "Beginner":
            return "Red"
        elif row["Certifications Completed"] < row["Certifications Enrolled"]:
            return "Amber"
        else:
            return "Green"
    df["Attrition Risk"] = df.apply(rag_status, axis=1)
    df_display = df.drop(columns=["Skills", "Peer Review", "Pre Training Scores", "Post Training Scores", "Trainings Assigned", "Trainings Completed", "Trainings Pending"])
    st.dataframe(df_display)

    st.subheader("Training Impact Across Team")
    for emp in employees:
        emp_skills = emp["Skills"]
        pre_scores = emp["Pre Training Scores"]
        post_scores = emp["Post Training Scores"]
        training_df = pd.DataFrame({
            "Pre-Training": [pre_scores[skill] for skill in emp_skills],
            "Post-Training": [post_scores[skill] for skill in emp_skills]
        }, index=emp_skills)
        st.markdown(f"**{emp['Name']}**")
        st.line_chart(training_df)

    st.subheader("Skill Proficiency vs Industry Standards")
    for emp in employees:
        emp_skills = emp["Skills"]
        post_scores = emp["Post Training Scores"]
        industry_levels = {skill: industry_standards.get(skill, 7) for skill in emp_skills}
        comparison_df = pd.DataFrame({
            "Employee": [post_scores[skill] for skill in emp_skills],
            "Industry": [industry_levels[skill] for skill in emp_skills]
        }, index=emp_skills)
        st.markdown(f"**{emp['Name']}**")
        st.bar_chart(comparison_df)

    st.subheader("Send Notification to Employee")
    selected_name = st.selectbox("Select Employee to Notify", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)
    default_message = f"Hi {selected_name}, please complete your pending trainings: {', '.join(selected_emp['Trainings Pending'])}."
    message = st.text_area("Notification Message", value=default_message)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {selected_name}: {message}")

