import json
import os
from datetime import datetime

# Initialize uploads folder globally
os.makedirs("uploads", exist_ok=True)

# ---------- DATA ----------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------- IMAGE SAVE ----------
def save_image(file, issue_id, event_type):
    if file is not None:
        path = f"uploads/{issue_id}_{event_type}.png"
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        return path
    return None

# ---------- TIME UTILITIES ----------
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_duration(start_time_str, end_time_str):
    fmt = "%Y-%m-%d %H:%M:%S"
    start = datetime.strptime(start_time_str, fmt)
    end = datetime.strptime(end_time_str, fmt)
    duration = end - start
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m"
