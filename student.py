import streamlit as st
from main import load_data, save_data, save_image, current_time

def student_panel():
    issues = load_data("issues.json")
    events = load_data("events.json")

    st.subheader("📌 Report Issue")

    issue_type = st.selectbox(
        "Issue Type",
        ["Water", "Electricity", "Food", "Hygiene"]
    )

    desc = st.text_input("Description (optional)")

    image = st.file_uploader(
        "Upload Proof (optional)",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Submit Issue"):
        issue_id = f"ISSUE{len(issues)+1}"
        time = current_time()

        img_path = save_image(image, issue_id, "reported")

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
            "time": time,
            "image": img_path
        })

        save_data("issues.json", issues)
        save_data("events.json", events)

        st.success(f"Issue {issue_id} submitted!")

    # -------- VIEW ISSUES --------
    st.subheader("📊 Your Issues")

    for issue in issues:
        st.markdown(f"### {issue['id']}")
        st.write(f"Status: {issue['status']}")

        for event in events:
            if event["issue_id"] == issue["id"]:
                st.write(f"{event['time']} → {event['event']}")

                if event.get("image"):
                    st.image(event["image"], width=200)
