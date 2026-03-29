import streamlit as st
import json
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(page_title="HostelOps", layout="centered")

# ---------- LOAD / SAVE ----------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

issues = load_data("issues.json")
events = load_data("events.json")

# ---------- HEADER ----------
st.title("🏠 HostelOps")
st.caption("Operational Accountability Platform")

# ---------- ROLE ----------
role = st.radio("Select Role", ["Student", "Admin"])

# =========================
# STUDENT PANEL
# =========================
if role == "Student":
    st.subheader("📌 Report an Issue")

    issue_type = st.selectbox(
        "Issue Type",
        ["Water", "Electricity", "Food", "Hygiene"]
    )

    desc = st.text_input("Description (optional)")
    image = st.file_uploader("Upload Proof (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit Issue"):
        issue_id = f"ISSUE{len(issues)+1}"
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        issues.append({
            "id": issue_id,
            "type": issue_type,
            "description": desc,
            "status": "Reported",
            "created_at": time
        })

        events.append({
            "issue_id": issue_id,
            "event": "Reported",
            "time": time
        })

        save_data("issues.json", issues)
        save_data("events.json", events)

        st.success(f"Issue {issue_id} submitted successfully!")

# =========================
# ADMIN PANEL
# =========================
elif role == "Admin":
    st.subheader("📋 All Issues")

    if not issues:
        st.info("No issues reported yet.")

    for issue in issues:
        with st.container():
            st.markdown(f"### {issue['id']}")
            st.write(f"Type: {issue['type']}")
            st.write(f"Status: {issue['status']}")
            st.write(f"Reported At: {issue['created_at']}")

            col1, col2 = st.columns(2)

            if col1.button(f"In Progress {issue['id']}"):
                issue["status"] = "In Progress"
                events.append({
                    "issue_id": issue["id"],
                    "event": "In Progress",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            if col2.button(f"Resolved {issue['id']}"):
                issue["status"] = "Resolved"
                events.append({
                    "issue_id": issue["id"],
                    "event": "Resolved",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    save_data("issues.json", issues)
    save_data("events.json", events)

    # ---------- TIMELINE ----------
    st.subheader("📈 Issue Timeline")

    if issues:
        selected_id = st.selectbox(
            "Select Issue",
            [i["id"] for i in issues]
        )

        st.write(f"### Timeline for {selected_id}")

        for event in events:
            if event["issue_id"] == selected_id:
                st.write(f"{event['time']} → {event['event']}")
