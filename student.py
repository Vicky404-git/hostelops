if issue["status"] == "Resolved":
    st.warning("⚠️ Please confirm if issue is resolved")

    col1, col2 = st.columns(2)

    if col1.button(f"Confirm Done {issue['id']}", key=f"confirm_{issue['id']}"):
        issue["status"] = "Confirmed"

        events.append({
            "issue_id": issue["id"],
            "event": "Confirmed by Student",
            "time": current_time()
        })

        save_data("issues.json", issues)
        save_data("events.json", events)

        st.success("Issue confirmed!")
        st.rerun()

    if col2.button(f"Not Done {issue['id']}", key=f"reopen_{issue['id']}"):
        issue["status"] = "Reopened"

        events.append({
            "issue_id": issue["id"],
            "event": "Reopened by Student",
            "time": current_time()
        })

        save_data("issues.json", issues)
        save_data("events.json", events)

        st.error("Issue reopened!")
        st.rerun()
