import os
from datetime import datetime

def current_time():
    """Returns formatted timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_image(file, issue_id, event_type):
    """Saves proof images to uploads/."""
    if file is not None:
        os.makedirs("uploads", exist_ok=True)
        path = f"uploads/{issue_id}_{event_type}.png"
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        return path
    return None

def calculate_duration(start_time_str, end_time_str):
    """Calculates resolution time for the Warden's Audit."""
    fmt = "%Y-%m-%d %H:%M:%S"
    start = datetime.strptime(start_time_str, fmt)
    end = datetime.strptime(end_time_str, fmt)
    duration = end - start
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m"
