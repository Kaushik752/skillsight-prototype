import streamlit as st
import pandas as pd
import random

# Simulated employee data
employee_data = [
    {"name": f"Employee {i+1}",
     "role": "Software Developer" if i < 10 else "Data Analyst",
     "skills": ["Python", "SQL", "Data Analysis"] if i >= 10 else ["Python", "Git", "APIs"],
     "upskill_needed": "Advanced Python" if i < 10 else None,
     "promotion_eligible": True if i in [15, 16, 17, 18, 19] else False,
     "peer_review": f"Peer feedback for Employee {i+1}: {random.choice(['Excellent team player', 'Needs improvement in communication', 'Strong technical skills', 'Collaborative and proactive'])}"
    }
    for i in range(20)
]

# Convert to DataFrame for display
df = pd.DataFrame(employee_data)

# Streamlit app layout
st.title("SkillSight - Employee Dashboard")

st.subheader("Employee Overview")
selected_employee = st.selectbox("Select an employee", df["name"].tolist())

# Display selected employee details
emp = df[df["name"] == selected_employee].iloc[0]
st.write(f"**Role:** {emp['role']}")
st.write(f"**Skills:** {', '.join(emp['skills'])}")
if emp["upskill_needed"]:
    st.write(f"**Upskill Needed:** {emp['upskill_needed']}")
st.write(f"**Promotion Eligible:** {'Yes' if emp['promotion_eligible'] else 'No'}")
st.write(f"**Peer Review:** {emp['peer_review']}")

# Display full employee table
st.subheader("All Employees Summary")
st.dataframe(df.drop(columns=["peer_review"]))  # Hide peer review in summary table for brevity



