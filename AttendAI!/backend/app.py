from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB = "attendai.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    role = data["role"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=? AND role=?",
        (username, password, role)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "role": role})
    return jsonify({"success": False})


# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO students VALUES (?,?,?,?)",
                (data["prn"], data["name"], data["course"], data["division"]))

    cur.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                (data["prn"], data["password"], "student"))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Student Added"})


# ---------------- GET STUDENTS ----------------
@app.route("/students")
def students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


# ---------------- STATS ----------------
@app.route("/api/stats")
def stats():
    conn = get_db()

    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")

    present = conn.execute(
        "SELECT COUNT(DISTINCT prn) FROM attendance WHERE date=?",
        (today,)
    ).fetchone()[0]

    conn.close()

    absent = total - present
    percent = (present/total*100) if total else 0

    return jsonify({
        "total_students": total,
        "present": present,
        "absent": absent,
        "attendance_percent": round(percent,2)
    })


# ---------------- REPORT ----------------
@app.route("/report", methods=["POST"])
def report():
    data = request.json
    course = data["course"]
    division = data["division"]
    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")

    conn = get_db()

    students = conn.execute(
        "SELECT prn,name FROM students WHERE course=? AND division=?",
        (course, division)
    ).fetchall()

    result = []

    for s in students:
        prn = s["prn"]

        row = conn.execute(
            "SELECT * FROM attendance WHERE prn=? AND date=?",
            (prn, date)
        ).fetchone()

        status = "Present" if row else "Absent"

        result.append({
            "prn": prn,
            "name": s["name"],
            "status": status
        })

    conn.close()
    return jsonify({"data": result})


# ---------------- MARK ATTENDANCE ----------------
@app.route("/mark", methods=["POST"])
def mark():
    data = request.json

    conn = get_db()

    conn.execute(
        "INSERT INTO attendance(prn,date,status) VALUES (?,?,?)",
        (data["prn"], datetime.now().strftime("%Y-%m-%d"), "Present")
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# ---------------- STUDENT HISTORY ----------------
@app.route("/student/<prn>")
def student_history(prn):
    conn = get_db()

    rows = conn.execute(
        "SELECT date,status FROM attendance WHERE prn=?",
        (prn,)
    ).fetchall()

    conn.close()

    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(debug=True)