# core/models.py
from core.database import get_db_connection
from core.utils import current_time


class HostelManager:
    """Handles all database transactions for HostelOps."""

    @staticmethod
    def get_all_events():
        """Fetches all events for the audit CSV export."""
        conn = get_db_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM events ORDER BY event_time DESC")
        events = cursor.fetchall()
        
        conn.close()
        return events
    
    @staticmethod
    def get_dashboard_metrics():
        """Fetches total, pending, and verified issue counts."""
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)
        
        metrics = {}
        cursor.execute("SELECT COUNT(*) AS total FROM issues")
        metrics['total'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) AS pending FROM issues WHERE current_status NOT IN ('Confirmed', 'Resolved')")
        metrics['pending'] = cursor.fetchone()['pending']
        
        cursor.execute("SELECT COUNT(*) AS verified FROM issues WHERE current_status = 'Confirmed'")
        metrics['verified'] = cursor.fetchone()['verified']
        
        conn.close()
        return metrics

    @staticmethod
    def log_issue(student_id, block, room, issue_type, desc, img_path):
        """Creates a new issue and its first event log."""
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor(dictionary=True)

        # Generate custom ID
        cursor.execute("SELECT COUNT(*) AS cnt FROM issues")
        count = cursor.fetchone()['cnt']
        issue_id = f"ISSUE{count + 1}"
        time = current_time()

        # Insert Issue
        cursor.execute("""
            INSERT INTO issues (issue_id, student_id, block, room, issue_type, description, current_status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (issue_id, student_id, block, room, issue_type, desc, "Reported", time))

        # Insert Initial Event
        cursor.execute("""
            INSERT INTO events (issue_id, event_desc, event_time, image_path)
            VALUES (%s, %s, %s, %s)
        """, (issue_id, "Reported", time, img_path))

        conn.commit()
        conn.close()
        return issue_id

    @staticmethod
    def update_status(issue_id, new_status, event_desc, img_path=None):
        """Updates an issue status and logs the event immutably."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE issues SET current_status = %s WHERE issue_id = %s", (new_status, issue_id))
        cursor.execute(
            "INSERT INTO events (issue_id, event_desc, event_time, image_path) VALUES (%s, %s, %s, %s)", 
            (issue_id, event_desc, current_time(), img_path)
        )
        conn.commit()
        conn.close()
