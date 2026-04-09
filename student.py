import streamlit as st
from main import load_data, save_data, save_image, current_time

def student_panel():
    issues = load_data("issues.json")
    events = load_data("events.json")

    # ---------------- REPORT ISSUE ----------------
    st.subheader("📌 Report an Issue")

    hostel_block = st.selectbox("Hostel Block", ["Block A (Boys)", "Block B (Boys)", "Block C (Girls)", "PG Hostel"])
    
    col1, col2 = st.columns(2)
    issue_type = col1.selectbox("Issue Type", ["Water", "Electricity", "Food", "Hygiene", "Infrastructure"])
    room_no = col2.text_input("Room Number")
    
    is_anonymous = st.checkbox("Keep my identity/room anonymous from ground staff")

    desc = st.text_area("Description (optional)")

    image = st.file_uploader("Upload Proof (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit Issue"):
        issue_id = f"ISSUE{len(issues)+1}"
        time = current_time()

        img_path = save_image(image, issue_id, "reported")

        issues.append({
            "id": issue_id,
            "block": hostel_block,
            "room": "Classified" if is_anonymous else room_no,
            "type": issue_type,
            "description": desc,
            "status": "Reported",
            "created_at": time
        })

        events.append({
            "issue_id": issue_id,
            "event": "Reported",
            "time": time,
            "image": img_path
        })

        save_data("issues.json", issues)
        save_data("events.json", events)

        st.success(f"Issue {issue_id} submitted successfully!")
        st.rerun()

    # ---------------- VIEW ISSUES ----------------
    st.divider()
    st.subheader("📊 Your Active Issues")

    for issue in issues:
        st.markdown(f"### {issue['id']}")
        st.write(f"**Status:** {issue['status']}")

        # -------- Timeline --------
        for event in events:
            if event["issue_id"] == issue["id"]:
                st.write(f"• {event['time']} → {event['event']}")
                if event.get("image"):
                    st.image(event["image"], width=150)

        # -------- CONFIRMATION LOOP --------
        if issue["status"] == "Resolved":
            st.warning("⚠️ Action Required: Please confirm if this issue is actually resolved.")

            col1, col2 = st.columns(2)

            if col1.button(f"Yes, it is fixed ({issue['id']})", key=f"confirm_{issue['id']}"):
                issue["status"] = "Confirmed"
                events.append({
                    "issue_id": issue["id"],
                    "event": "Confirmed by Student",
                    "time": current_time()
                })
                save_data("issues.json", issues)
                save_data("events.json", events)
                st.success("Issue closed!")
                st.rerun()

            if col2.button(f"No, it is NOT fixed ({issue['id']})", key=f"reopen_{issue['id']}"):
                issue["status"] = "Reopened"
                events.append({
                    "issue_id": issue["id"],
                    "event": "Reopened by Student (Escalated)",
                    "time": current_time()
                })
                save_data("issues.json", issues)
                save_data("events.json", events)
                st.error("Issue reopened and escalated to Warden!")
                st.rerun()
