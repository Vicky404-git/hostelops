import json
import os
from datetime import datetime

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
        os.makedirs("uploads", exist_ok=True)
        path = f"uploads/{issue_id}_{event_type}.png"
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        return path
    return None

# ---------- TIME ----------
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
