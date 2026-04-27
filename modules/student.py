import streamlit as st
from core.database import get_db_connection
from core.utils import current_time, save_image

def student_panel(student_id):
    st.subheader(f"📌 Report an Issue (User: {student_id})")

    hostel_block = st.selectbox("Hostel Block", ["Block A (Boys)", "Block B (Boys)", "Block C (Girls)", "PG Hostel"])
    
    col1, col2 = st.columns(2)
    issue_type = col1.selectbox("Issue Type", ["Water", "Electricity", "Food", "Hygiene", "Infrastructure"])
    room_no = col2.text_input("Room Number")
    
    is_anonymous = st.checkbox("Keep my identity/room anonymous from ground staff")
    desc = st.text_area("Description (optional)")
    image = st.file_uploader("Upload Proof (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit Issue"):
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS cnt FROM issues")
        count = cursor.fetchone()['cnt']
        issue_id = f"ISSUE{count + 1}"
        
        time = current_time()
        img_path = save_image(image, issue_id, "reported")
        final_room = "Classified" if is_anonymous else room_no

        cursor.execute("""
            INSERT INTO issues (issue_id, student_id, block, room, issue_type, description, current_status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (issue_id, student_id, hostel_block, final_room, issue_type, desc, "Reported", time))

        cursor.execute("""
            INSERT INTO events (issue_id, event_desc, event_time, image_path)
            VALUES (%s, %s, %s, %s)
        """, (issue_id, "Reported", time, img_path))

        conn.commit()
        conn.close()

        st.success(f"Issue {issue_id} submitted successfully!")
        st.rerun()

    st.divider()
    st.subheader("📊 Your Active Issues")

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM issues WHERE student_id = %s", (student_id,))
    my_issues = cursor.fetchall()

    if not my_issues:
        st.info("You have not reported any issues yet.")

    for issue in my_issues:
        st.markdown(f"### {issue['issue_id']}")
        st.write(f"**Status:** {issue['current_status']}")

        cursor.execute("SELECT * FROM events WHERE issue_id = %s ORDER BY event_time ASC", (issue['issue_id'],))
        events = cursor.fetchall()

        for event in events:
            st.write(f"• {event['event_time']} → {event['event_desc']}")
            if event.get("image_path"):
                st.image(event["image_path"], width=150)

        if issue["current_status"] == "Resolved":
            st.warning("⚠️ Action Required: Please confirm if this issue is actually resolved.")
            col1, col2 = st.columns(2)

            if col1.button(f"Yes, it is fixed ({issue['issue_id']})"):
                cursor.execute("UPDATE issues SET current_status = 'Confirmed' WHERE issue_id = %s", (issue['issue_id'],))
                cursor.execute("INSERT INTO events (issue_id, event_desc, event_time) VALUES (%s, %s, %s)", (issue['issue_id'], "Confirmed by Student", current_time()))
                conn.commit()
                st.success("Issue closed!")
                st.rerun()

            if col2.button(f"No, it is NOT fixed ({issue['issue_id']})"):
                cursor.execute("UPDATE issues SET current_status = 'Reopened' WHERE issue_id = %s", (issue['issue_id'],))
                cursor.execute("INSERT INTO events (issue_id, event_desc, event_time) VALUES (%s, %s, %s)", (issue['issue_id'], "Reopened by Student (Escalated)", current_time()))
                conn.commit()
                st.error("Issue reopened and escalated to Warden!")
                st.rerun()
    conn.close()
