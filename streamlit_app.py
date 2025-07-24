import streamlit as st
import pandas as pd

# Sample data for 20 employees
employees = [
    {"name": f"Employee {i+1}",
     "role": "Software Developer" if i < 10 else "QA Engineer",
     "skills": ["Python", "Git", "APIs"] if i < 10 else ["Testing", "Automation"],
     "peer_review": "Strong team player with good collaboration." if i % 2 == 0 else "Needs improvement in communication.",
     "promotion_eligible": True if i in [2, 4, 6, 12, 15] else False,
     "communication_skills": "Excellent" if i % 3 == 0 else "Good" if i % 3 == 1 else "Average"
    }
    for i in range(20)
]

# Convert to DataFrame for summary view
df = pd.DataFrame(employees)

# Streamlit App
st.title("SkillSight - Employee Dashboard")

# Dropdown to select employee
selected_employee = st.selectbox("Select an Employee", df["name"])

# Display selected employee details
emp = df[df["name"] == selected_employee].iloc[0]
st.subheader(f"Profile: {emp['name']}")
st.write(f"**Role:** {emp['role']}")
st.write(f"**Skills:** {', '.join(emp['skills'])}")
st.write(f"**Peer Review:** {emp['peer_review']}")
st.write(f"**Communication Skills:** {emp['communication_skills']}")
st.write(f"**Promotion Eligible:** {'Yes' if emp['promotion_eligible'] else 'No'}")

# Summary table
st.subheader("Team Overview")
st.dataframe(df.drop(columns=["peer_review"]))

