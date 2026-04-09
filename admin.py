import streamlit as st
from main import load_data, save_data, save_image, current_time

def admin_panel():
    # 1. LOAD DATA FIRST (Must happen before you calculate metrics)
    issues = load_data("issues.json")
    events = load_data("events.json")

    # 2. WARDEN'S DASHBOARD
    st.subheader("📊 Warden's Dashboard")
    
    # Quick Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Issues", len(issues))
    col2.metric("Pending", len([i for i in issues if i.get('status') != 'Confirmed']))
    col3.metric("Fully Resolved", len([i for i in issues if i.get('status') == 'Confirmed']))

    # Simple Bar Chart for Issue Types
    issue_counts = {}
    for i in issues:
        issue_counts[i['type']] = issue_counts.get(i['type'], 0) + 1
    
    # Only try to draw the chart if there is actual data
    if issue_counts:
        st.bar_chart(issue_counts)
        
    st.divider()

    # 3. ISSUE MANAGEMENT
    st.subheader("📋 All Issues")

    if not issues:
        st.info("No issues yet.")

    for issue in issues:
        with st.container():
            st.markdown(f"### {issue['id']}")
            st.write(f"Type: {issue['type']}")
            st.write(f"Status: {issue['status']}")

            img_progress = st.file_uploader(
                f"Upload Progress Proof ({issue['id']})",
                key=f"prog_{issue['id']}"
            )

            img_resolved = st.file_uploader(
                f"Upload Resolution Proof ({issue['id']})",
                key=f"res_{issue['id']}"
            )

            col1, col2 = st.columns(2)

            if col1.button(f"In Progress {issue['id']}"):
                path = save_image(img_progress, issue["id"], "progress")

                issue["status"] = "In Progress"
                events.append({
                    "issue_id": issue["id"],
                    "event": "In Progress",
                    "time": current_time(),
                    "image": path
                })
                # Save immediately and rerun to update dashboard
                save_data("issues.json", issues)
                save_data("events.json", events)
                st.rerun()

            if col2.button(f"Resolved {issue['id']}"):
                path = save_image(img_resolved, issue["id"], "resolved")

                issue["status"] = "Resolved"
                events.append({
                    "issue_id": issue["id"],
                    "event": "Resolved",
                    "time": current_time(),
                    "image": path
                })
                # Save immediately and rerun to update dashboard
                save_data("issues.json", issues)
                save_data("events.json", events)
                st.rerun()


    # 4. TIMELINE
    st.subheader("📈 Timeline")

    if issues:
        selected_id = st.selectbox(
            "Select Issue",
            [i["id"] for i in issues]
        )

        for event in events:
            if event["issue_id"] == selected_id:
                st.write(f"{event['time']} → {event['event']}")
                if event.get("image"):
                    st.image(event["image"], width=200)
