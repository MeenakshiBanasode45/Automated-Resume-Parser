"""
database.py - Database operations for the Automated Resume Parser.
Uses Python's built-in SQLite3 module to store and retrieve candidate details.
"""

import sqlite3

# Name of the SQLite database file
DB_NAME = "candidates.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Initializes the database and creates the 'candidates' table if it does not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_candidate(name, email, phone, skills, education):
    """
    Inserts a newly parsed candidate record into the candidates table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates (name, email, phone, skills, education)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, skills, education))
    conn.commit()
    conn.close()


def get_all_candidates():
    """
    Retrieves all candidate records from the database in descending order of ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, phone, skills, education 
        FROM candidates 
        ORDER BY id DESC
    """)
    records = cursor.fetchall()
    conn.close()
    return records


def search_candidates(keyword):
    """
    Searches candidates whose name or skills contain the given keyword.
    """
    conn = get_connection()
    cursor = conn.cursor()
    search_pattern = f"%{keyword}%"
    cursor.execute("""
        SELECT id, name, email, phone, skills, education 
        FROM candidates 
        WHERE name LIKE ? OR skills LIKE ?
        ORDER BY id DESC
    """, (search_pattern, search_pattern))
    records = cursor.fetchall()
    conn.close()
    return records
