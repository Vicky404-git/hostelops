# 🏠 HostelOps

**Event-Driven Institutional Operations Accountability System**

HostelOps is a structured digital platform designed to manage institutional workflows (hostels, hospitals, residential facilities). Moving beyond simple grievance portals, it utilizes an append-only, event-driven architecture to ensure complete operational transparency, verified issue resolution, and staff accountability.

## ✨ Core Features

* **Immutable Audit Trail:** Every action (reporting, assigning, resolving) is logged as a time-stamped event. History cannot be overwritten.
* **Role-Based Access Control (RBAC):** Dedicated portals for Students (reporting/verification) and Wardens (assignment/analytics).
* **Proof of Work:** Mandatory photo uploads for resolving maintenance issues.
* **Closed-Loop Escalation:** Issues are only closed when verified by the reporting student; otherwise, they are escalated.
* **Automated SLA Tracking:** Automatically calculates "Time to Resolution" metrics for administrative auditing.

## 🛠️ Technical Stack

* **Frontend/UI:** Streamlit (Python)
* **Database:** MariaDB / MySQL (Relational)
* **Package Manager:** `uv`
* **Architecture:** Modular MVC-style pattern

## 📂 Project Structure

```text
hostelops/
├── app.py                 # Main entry point and routing
├── core/                  # Core backend logic
│   ├── database.py        # Secure MariaDB connection handling
│   └── utils.py           # Time formatting, image saving, and SLA calculations
├── modules/               # UI Panels
│   ├── admin.py           # Warden dashboard, analytics, and staff assignment
│   └── student.py         # Issue reporting and resolution verification
├── sql/                   # Database Migrations
│   └── schema.sql         # Table structures (issues, events) and relations
├── uploads/               # Local storage for image proof
├── .env                   # Environment variables (DB credentials)
└── requirements.txt / uv.lock
```

## 🚀 Installation & Setup

### 1. Prerequisites

* Python 3.10+ (Tested on 3.13)
* MariaDB or MySQL Server installed locally or remotely
* `uv` package manager (recommended)

### 2. Database Setup

Create the database and necessary tables by executing the schema file. Log into your MariaDB instance and run:

```bash
sudo mysql -u root < sql/schema.sql
```

*Note: We recommend creating a dedicated database user (e.g., `hostel_admin`) with privileges granted to `hostelops_db` rather than using `root`.*

### 3. Environment Configuration

Create a `.env` file in the root directory and configure your database credentials:

```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASS=your_secure_password
DB_NAME=hostelops_db
```

### 4. Install Dependencies

Install the required packages (Streamlit, MySQL Connector, Python-Dotenv) using `uv`:

```bash
uv add streamlit mysql-connector-python python-dotenv
```

### 5. Run the Application

Launch the Streamlit server:

```bash
uv run streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. Copyright (c) 2026 Vikas Dhruw.

