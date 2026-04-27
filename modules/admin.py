import streamlit as st
from core.database import get_db_connection
from core.utils import current_time, save_image, calculate_duration

def admin_panel():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor(dictionary=True)

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Warden's Dashboard")
    
    cursor.execute("SELECT COUNT(*) AS total FROM issues")
    total_issues = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) AS pending FROM issues WHERE current_status NOT IN ('Confirmed', 'Resolved')")
    pending_issues = cursor.fetchone()['pending']
    
    cursor.execute("SELECT COUNT(*) AS verified FROM issues WHERE current_status = 'Confirmed'")
    verified_issues = cursor.fetchone()['verified']

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Issues", total_issues)
    col2.metric("Pending/Open", pending_issues)
    col3.metric("Fully Verified", verified_issues)

    cursor.execute("SELECT issue_type, COUNT(*) as count FROM issues GROUP BY issue_type")
    type_counts = cursor.fetchall()
    if type_counts:
        chart_data = {row['issue_type']: row['count'] for row in type_counts}
        st.bar_chart(chart_data)
        
    st.divider()

    # ---------------- ISSUE MANAGEMENT ----------------
    st.subheader("📋 Operational Backlog")

    cursor.execute("SELECT * FROM issues ORDER BY CASE WHEN current_status = 'Reopened' THEN 0 ELSE 1 END, created_at DESC")
    issues = cursor.fetchall()

    if not issues:
        st.info("No issues yet. The hostel is running smoothly!")

    for issue in issues:
        with st.container():
            if issue['current_status'] == "Reopened":
                st.error(f"⚠️ ESCALATED: {issue['issue_id']} (Student reported this was NOT actually fixed)")
            else:
                st.markdown(f"### {issue['issue_id']}")
            
            st.write(f"**Location:** {issue['block']} - Room {issue['room']}")
            st.write(f"**Type:** {issue['issue_type']} | **Status:** {issue['current_status']}")
            if issue.get('description'):
                st.caption(f"Details: {issue['description']}")

            if issue['current_status'] == 'Confirmed':
                st.success("✅ This issue has been verified and closed by the student.")
            else:
                worker = st.selectbox(
                    "Assign Staff", 
                    ["Maintenance Team Alpha", "Plumber Ram", "Electrician Shyam", "Cleaning Staff"], 
                    key=f"worker_{issue['issue_id']}"
                )

                img_progress = st.file_uploader(f"Upload Progress Proof ({issue['issue_id']})", key=f"prog_{issue['issue_id']}")
                img_resolved = st.file_uploader(f"Upload Resolution Proof ({issue['issue_id']})", key=f"res_{issue['issue_id']}")

                col1, col2 = st.columns(2)
                
                if col1.button(f"Assign & Start ({issue['issue_id']})"):
                    path = save_image(img_progress, issue['issue_id'], "progress") if img_progress else None
                    new_status = f"In Progress ({worker})"
                    event_desc = f"Assigned to {worker} - Work Started"

                    cursor.execute("UPDATE issues SET current_status = %s WHERE issue_id = %s", (new_status, issue['issue_id']))
                    cursor.execute("INSERT INTO events (issue_id, event_desc, event_time, image_path) VALUES (%s, %s, %s, %s)", (issue['issue_id'], event_desc, current_time(), path))
                    conn.commit()
                    st.rerun()

                if col2.button(f"Mark Resolved ({issue['issue_id']})"):
                    path = save_image(img_resolved, issue['issue_id'], "resolved") if img_resolved else None

                    cursor.execute("UPDATE issues SET current_status = 'Resolved' WHERE issue_id = %s", (issue['issue_id'],))
                    cursor.execute("INSERT INTO events (issue_id, event_desc, event_time, image_path) VALUES (%s, %s, %s, %s)", (issue['issue_id'], "Resolved by Staff", current_time(), path))
                    conn.commit()
                    st.rerun()
        st.write("---")

    # ---------------- TIMELINE & AUDIT ----------------
    st.subheader("📈 Accountability Audit")

    if issues:
        selected_id = st.selectbox("Select Issue to Audit", [i["issue_id"] for i in issues])
        
        cursor.execute("SELECT * FROM events WHERE issue_id = %s ORDER BY event_time ASC", (selected_id,))
        issue_events = cursor.fetchall()
        
        for event in issue_events:
            st.write(f"{event['event_time']} → **{event['event_desc']}**")
            if event.get("image_path"):
                st.image(event["image_path"], width=200)
                
        if len(issue_events) > 0 and any("Resolved" in e["event_desc"] or "Confirmed" in e["event_desc"] for e in issue_events):
            start = str(issue_events[0]["event_time"])
            end_events = [e for e in issue_events if "Resolved" in e["event_desc"]]
            if end_events:
                end = str(end_events[0]["event_time"])
                try:
                    duration = calculate_duration(start, end)
                    st.success(f"⏱️ **Time to Resolution:** {duration}")
                except Exception:
                    pass
    conn.close()
