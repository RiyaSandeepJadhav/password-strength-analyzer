import sqlite3
import hashlib
from datetime import datetime

DATABASE_NAME = "password_history.db"


# -----------------------------------------
# Create Database
# -----------------------------------------

def init_db():
    """
    Creates the database and table if they do not exist.
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            password_hash TEXT UNIQUE NOT NULL,

            created_at TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# Hash Password
# -----------------------------------------

def hash_password(password):
    """
    Convert password to SHA-256 hash.
    """

    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------------------
# Save Password
# -----------------------------------------

def save_password(password):
    """
    Stores only the SHA-256 hash of the password.
    """

    password_hash = hash_password(password)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:

        cursor.execute("""

            INSERT INTO password_history
            (password_hash, created_at)

            VALUES (?, ?)

        """, (

            password_hash,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ))

        conn.commit()

    except sqlite3.IntegrityError:
        # Password already exists
        pass

    finally:
        conn.close()


# -----------------------------------------
# Check Password Reuse
# -----------------------------------------

def password_exists(password):
    """
    Returns True if password hash already exists.
    """

    password_hash = hash_password(password)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id

        FROM password_history

        WHERE password_hash = ?

    """, (

        password_hash,

    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None


# -----------------------------------------
# Password Count
# -----------------------------------------

def total_passwords():
    """
    Returns total passwords stored.
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM password_history

    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


# -----------------------------------------
# Clear Database
# -----------------------------------------

def clear_database():
    """
    Deletes all password history.
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM password_history

    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# Show Password History (Hashes Only)
# -----------------------------------------

def get_password_history():
    """
    Returns all stored password hashes.
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            id,
            password_hash,
            created_at

        FROM password_history

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    init_db()

    password = "Example@123"

    if password_exists(password):
        print("Password already used.")

    else:
        save_password(password)
        print("Password saved.")

    print("\nStored Password Hashes:\n")

    for row in get_password_history():
        print(row)

    print("\nTotal Passwords:", total_passwords())