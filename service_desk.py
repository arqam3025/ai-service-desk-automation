"""Deterministic, explainable service-desk triage and SQLite workflow demo."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

SCHEMA="""CREATE TABLE IF NOT EXISTS tickets(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 subject TEXT NOT NULL,
 description TEXT NOT NULL,
 priority TEXT NOT NULL,
 team TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'open',
 created_at TEXT NOT NULL
);"""

def triage(subject,description):
    text=f"{subject} {description}".lower()
    if any(word in text for word in ("outage","production down","data breach","ransomware")):
        return "P1","Incident Response"
    if any(word in text for word in ("login","password","access","account")):
        return "P2","Identity & Access"
    if any(word in text for word in ("invoice","billing","payment")):
        return "P3","Billing"
    return "P3","General Support"

def connect(path="tickets.db"):
    db=sqlite3.connect(path)
    db.execute(SCHEMA)
    db.commit()
    return db

def submit_ticket(db,subject,description):
    if not subject.strip() or not description.strip():
        raise ValueError("Subject and description are required")
    priority,team=triage(subject,description)
    created=datetime.now(timezone.utc).isoformat()
    cur=db.execute("INSERT INTO tickets(subject,description,priority,team,created_at) VALUES(?,?,?,?,?)",
                   (subject.strip(),description.strip(),priority,team,created))
    db.commit()
    return cur.lastrowid

def update_status(db,ticket_id,status):
    if status not in {"open","in_progress","resolved"}:
        raise ValueError("Invalid status")
    cur=db.execute("UPDATE tickets SET status=? WHERE id=?",(status,ticket_id))
    db.commit()
    return cur.rowcount

def get_tickets(db):
    return db.execute("SELECT id,subject,priority,team,status,created_at FROM tickets ORDER BY id DESC").fetchall()
