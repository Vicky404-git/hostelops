import streamlit as st
from main import load_data, save_data, save_image, current_time, calculate_duration

def admin_panel():
    issues = load_data("issues.json")
    events = load_data("events.json")

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Warden's Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Issues", len(issues))
    col2.metric("Pending/Open", len([i for i in issues if i.get('status') not in ['Confirmed', 'Resolved']]))
    col3.metric("Fully Verified", len([i for i in issues if i.get('status') == 'Confirmed']))

    issue_counts = {}
    for i in issues:
        issue_counts[i['type']] = issue_counts.get(i['type'], 0) + 1
    
    if issue_counts:
        st.bar_chart(issue_counts)
        
    st.divider()

    # ---------------- ISSUE MANAGEMENT ----------------
    st.subheader("📋 Operational Backlog")

    if not issues:
        st.info("No issues yet. The hostel is running smoothly!")

    # Sort issues so 'Reopened' ones appear at the top
    issues_sorted = sorted(issues, key=lambda x: 0 if x.get('status') == 'Reopened' else 1)

    for issue in issues_sorted:
        with st.container():
            # Escalation Flagging
            if issue.get('status') == "Reopened":
                st.error(f"⚠️ ESCALATED: {issue['id']} (Student reported this was NOT actually fixed)")
            else:
                st.markdown(f"### {issue['id']}")
            
            st.write(f"**Location:** {issue.get('block', 'Unknown')} - Room {issue.get('room', 'Unknown')}")
            st.write(f"**Type:** {issue['type']} | **Status:** {issue['status']}")
            if issue.get('description'):
                st.caption(f"Details: {issue['description']}")

            # Hide action buttons if the issue is completely verified
            if issue.get('status') == 'Confirmed':
                st.success("✅ This issue has been verified and closed by the student.")
            else:
                # Assignment Dropdown
                worker = st.selectbox(
                    "Assign Staff", 
                    ["Maintenance Team Alpha", "Plumber Ram", "Electrician Shyam", "Cleaning Staff"], 
                    key=f"worker_{issue['id']}"
                )

                # Streamlit Fix: File uploaders must be rendered OUTSIDE the button clicks
                img_progress = st.file_uploader(f"Upload Progress Proof ({issue['id']})", key=f"prog_{issue['id']}")
                img_resolved = st.file_uploader(f"Upload Resolution Proof ({issue['id']})", key=f"res_{issue['id']}")

                col1, col2 = st.columns(2)
                
                # Action Buttons
                if col1.button(f"Assign & Start ({issue['id']})", key=f"start_{issue['id']}"):
                    path = save_image(img_progress, issue["id"], "progress") if img_progress else None

                    issue["status"] = f"In Progress ({worker})"
                    events.append({
                        "issue_id": issue["id"],
                        "event": f"Assigned to {worker} - Work Started",
                        "time": current_time(),
                        "image": path
                    })
                    save_data("issues.json", issues)
                    save_data("events.json", events)
                    st.rerun()

                if col2.button(f"Mark Resolved ({issue['id']})", key=f"resolve_{issue['id']}"):
                    path = save_image(img_resolved, issue["id"], "resolved") if img_resolved else None

                    issue["status"] = "Resolved"
                    events.append({
                        "issue_id": issue["id"],
                        "event": "Resolved by Staff",
                        "time": current_time(),
                        "image": path
                    })
                    save_data("issues.json", issues)
                    save_data("events.json", events)
                    st.rerun()
        st.write("---")

    # ---------------- TIMELINE & AUDIT ----------------
    st.subheader("📈 Accountability Audit")

    if issues:
        selected_id = st.selectbox("Select Issue to Audit", [i["id"] for i in issues])
        
        issue_events = [e for e in events if e["issue_id"] == selected_id]
        
        for event in issue_events:
            st.write(f"{event['time']} → **{event['event']}**")
            if event.get("image"):
                st.image(event["image"], width=200)
                
        # Calculate SLA / Resolution Time
        if len(issue_events) > 0 and any("Resolved" in e["event"] or "Confirmed" in e["event"] for e in issue_events):
            start = issue_events[0]["time"]
            # Find the time it was marked resolved
            end_events = [e for e in issue_events if "Resolved" in e["event"]]
            if end_events:
                end = end_events[0]["time"]
                try:
                    duration = calculate_duration(start, end)
                    st.success(f"⏱️ **Time to Resolution:** {duration}")
                except Exception:
                    pass
