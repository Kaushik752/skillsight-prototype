import streamlit as st
import pandas as pd
import random

# Simulate employee data
def generate_employee_data():
    roles = ['Software Developer', 'Data Analyst', 'QA Engineer', 'Product Manager']
    skills = ['Python', 'SQL', 'Testing', 'Project Management', 'Advanced Python']
    data = []

    for i in range(1, 21):
        role = 'Software Developer' if i <= 10 else random.choice(roles)
        skill_set = ['Python'] if role == 'Software Developer' else random.sample(skills, 2)
        if role == 'Software Developer':
            skill_set.append('Advanced Python')  # simulate upskilling need
        promotion_eligible = True if i in [1, 2, 3, 4, 5] else False
        data.append({
            'Employee ID': f'EMP{i:03}',
            'Name': f'Employee {i}',
            'Role': role,
            'Skills': ', '.join(skill_set),
            'Promotion Eligible': promotion_eligible
        })

    return pd.DataFrame(data)

# Streamlit app
st.title("SkillSight Prototype Dashboard")

df = generate_employee_data()

st.subheader("Employee Overview")
st.dataframe(df)

st.subheader("Promotion Eligibility Summary")
promotion_count = df['Promotion Eligible'].sum()
st.write(f"Total Employees Eligible for Promotion: {promotion_count}")

st.subheader("Upskilling Needs")
upskill_df = df[df['Skills'].str.contains('Advanced Python')]
st.write(f"Employees Needing Upskilling in Advanced Python: {len(upskill_df)}")
st.dataframe(upskill_df[['Employee ID', 'Name', 'Role', 'Skills']])

# Save the corrected version
with open("streamlit_app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd
import random

# Simulate employee data
def generate_employee_data():
    roles = ['Software Developer', 'Data Analyst', 'QA Engineer', 'Product Manager']
    skills = ['Python', 'SQL', 'Testing', 'Project Management', 'Advanced Python']
    data = []

    for i in range(1, 21):
        role = 'Software Developer' if i <= 10 else random.choice(roles)
        skill_set = ['Python'] if role == 'Software Developer' else random.sample(skills, 2)
        if role == 'Software Developer':
            skill_set.append('Advanced Python')  # simulate upskilling need
        promotion_eligible = True if i in [1, 2, 3, 4, 5] else False
        data.append({
            'Employee ID': f'EMP{i:03}',
            'Name': f'Employee {i}',
            'Role': role,
            'Skills': ', '.join(skill_set),
            'Promotion Eligible': promotion_eligible
        })

    return pd.DataFrame(data)

# Streamlit app
st.title("SkillSight Prototype Dashboard")

df = generate_employee_data()

st.subheader("Employee Overview")
st.dataframe(df)

st.subheader("Promotion Eligibility Summary")
promotion_count = df['Promotion Eligible'].sum()
st.write(f"Total Employees Eligible for Promotion: {promotion_count}")

st.subheader("Upskilling Needs")
upskill_df = df[df['Skills'].str.contains('Advanced Python')]
st.write(f"Employees Needing Upskilling in Advanced Python: {len(upskill_df)}")
st.dataframe(upskill_df[['Employee ID', 'Name', 'Role', 'Skills']])
""")

