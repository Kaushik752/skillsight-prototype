import streamlit as st
import pandas as pd
import random
from io import BytesIO
from PIL import Image
import base64

# Generate a simple Superman-style "S" logo with text
from matplotlib import pyplot as plt

def generate_logo():
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.text(0.5, 0.5, 'S', fontsize=80, fontweight='bold', color='red', ha='center', va='center')
    ax.axis('off')
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', transparent=True)
    buf.seek(0)
    return buf

# Save logo to file
logo_buf = generate_logo()
logo_image = Image.open(logo_buf)
logo_path = "skillsight_logo.png"
logo_image.save(logo_path)

# Encode logo image to base64 for embedding
with open(logo_path, "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

# Create the final Streamlit app code with embedded logo
app_code = f"""
import streamlit as st
import pandas as pd
import random
import base64

# Embed logo
logo_base64 = "{encoded_logo}"
st.markdown(
    f'<div style="display:flex; align-items:center;">'
    f'<img src="data:image/png;base64,{{logo_base64}}" width="60" style="margin-right:10px;">'
    f'<h1 style="color:#FF4B4B;">SkillSight Dashboard</h1>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("### Powered by Innovaccer-GE-OPs Team")

# Sample data generation
roles = [
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer",
    "Software Developer", "Data Analyst", "Project Manager", "QA Engineer", "DevOps Engineer"
]
skills_pool = ["Python", "SQL", "Communication", "Leadership", "Cloud", "Advanced Python", "Data Visualization"]
industry_standards = {{skill: random.randint(6, 9) for skill in skills_pool}}

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
    completed_trainings = random.sample(skills, completed)
    pending_trainings = list(set(skills) - set(completed_trainings))
    promotion = "Yes" if i < 5 else "No"
    pre_training_scores = {{skill: random.randint(4, 8) for skill in skills}}
    post_training_scores = {{skill: min(pre_training_scores[skill] + random.randint(0, 3), 10) for skill in skills}}
    employees.append({{
        "Name": f"Employee {{i+1}}",
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
    }})

# View toggle
view_mode = st.sidebar.radio("Select View Mode", ["Employee View", "Manager View"])

if view_mode == "Employee View":
    selected_name = st.sidebar.selectbox("Select Employee", [emp["Name"] for emp in employees])
    selected_emp = next(emp for emp in employees if emp["Name"] == selected_name)

    st.subheader(f"Profile: {{selected_name}}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Role:** {{selected_emp['Role']}}")
        st.markdown(f"**Experience:** {{selected_emp['Experience']}} years")
        st.markdown(f"**Communication Skills:** {{selected_emp['Communication']}}")
    with col2:
        st.markdown(f"**Skills:** {{', '.join(selected_emp['Skills'])}}")
        st.markdown(f"**Certifications Enrolled:** {{selected_emp['Certifications Enrolled']}}")
        st.markdown(f"**Certifications Completed:** {{selected_emp['Certifications Completed']}}")

    st.markdown("**Completed Trainings:**")
    st.write(selected_emp["Completed Trainings"])
    st.markdown("**Pending Trainings:**")
    st.write(selected_emp["Pending Trainings"])

    st.markdown("### Bot Notification")
    if selected_emp["Pending Trainings"]:
        st.info(f"Hi {{selected_name}}, you have pending trainings: {{', '.join(selected_emp['Pending Trainings'])}}. Please complete them soon!")

else:
    st.subheader("Manager View")
    df = pd.DataFrame(employees)
    df["Attrition Risk"] = df.apply(lambda row: "Red" if row["Certifications Completed"] < row["Certifications Enrolled"]/2 and row["Communication"] == "Beginner" else ("Amber" if row["Certifications Completed"] < row["Certifications Enrolled"] else "Green"), axis=1)
    df_display = df[["Name", "Role", "Experience", "Communication", "Peer Review", "Certifications Enrolled", "Certifications Completed", "Promotion Eligible", "Attrition Risk", "Completed Trainings", "Pending Trainings"]]
    st.dataframe(df_display)

    st.markdown("### Skill Growth Rate")
    growth_data = []
    for emp in employees:
        pre = emp["Pre Training Scores"]
        post = emp["Post Training Scores"]
        growth = sum(post[s] - pre[s] for s in pre) / len(pre)
        growth_data.append({{"Name": emp["Name"], "Skill Growth Rate": round(growth, 2)}})
    growth_df = pd.DataFrame(growth_data)
    st.bar_chart(growth_df.set_index("Name"))

    st.markdown("### Notify Employee")
    notify_name = st.selectbox("Select Employee to Notify", [emp["Name"] for emp in employees])
    notify_emp = next(emp for emp in employees if emp["Name"] == notify_name)
    default_msg = f"Hi {{notify_name}}, please complete your pending trainings: {{', '.join(notify_emp['Pending Trainings'])}}."
    message = st.text_area("Notification Message", value=default_msg)
    if st.button("Send Notification"):
        st.success(f"Notification sent to {{notify_name}}!")
"""

# Save the final app code to file
with open("streamlit_app.py", "w") as f:
    f.write(app_code)

