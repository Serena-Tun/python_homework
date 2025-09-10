import sqlite3
import os

DB_PATH = os.path.join("..", "db", "magazines.db")

# Task 1
def create_connection():
    """Create and return a database connection."""
    conn = None
    try:
        os.makedirs(os.path.join("..", "db"), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = 1")  # ✅ enforce FK constraints
        print(f"Connected to {DB_PATH}")
    except sqlite3.Error as e:
        print(f"Error while connecting to database: {e}")
    return conn

# Task 2
def create_tables(conn):
    """Create publishers, magazines, subscribers, subscriptions tables."""
    cur = conn.cursor()

    statements = [
        """
        CREATE TABLE IF NOT EXISTS publishers (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS magazines (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            address TEXT NOT NULL,
            UNIQUE(name, address)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id   INTEGER NOT NULL,
            magazine_id     INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE CASCADE,
            FOREIGN KEY (magazine_id)   REFERENCES magazines(id) ON DELETE CASCADE,
            UNIQUE (subscriber_id, magazine_id)
        );
        """
    ]

    for stmt in statements:
        try:
            cur.execute(stmt)
        except sqlite3.Error as e:
            print(f"SQL error: {e}")

    conn.commit()

# Task 3
def add_publisher(conn, name):
    try:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
        # Always fetch the correct ID
        cur.execute("SELECT id FROM publishers WHERE name = ?", (name,))
        return cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Error adding publisher: {e}")

def add_magazine(conn, name, publisher_id):
    try:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        conn.commit()
        # Fetch correct magazine ID
        cur.execute("SELECT id FROM magazines WHERE name = ?", (name,))
        return cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Error adding magazine: {e}")

def add_subscriber(conn, name, address):
    try:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
        # Fetch correct subscriber ID
        cur.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
        return cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")

def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO subscriptions (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
        """, (subscriber_id, magazine_id, expiration_date))
        conn.commit()
        # Fetch correct subscription ID
        cur.execute("""
            SELECT id FROM subscriptions 
            WHERE subscriber_id = ? AND magazine_id = ?
        """, (subscriber_id, magazine_id))
        return cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")

# Task 4 
def get_all_subscribers(conn):
    print("\nSubscribers:")
    cur = conn.cursor()
    cur.execute("SELECT * FROM subscribers;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def get_all_magazines_sorted(conn):
    print("\nMagazines (sorted by name):")
    cur = conn.cursor()
    cur.execute("SELECT * FROM magazines ORDER BY name;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def get_magazines_by_publisher(conn, publisher_name):
    print(f"\nMagazines published by {publisher_name}:")
    cur = conn.cursor()
    query = """
        SELECT magazines.id, magazines.name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?;
    """
    cur.execute(query, (publisher_name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# -----------------------------
# Main Program
# -----------------------------
def main():
    conn = create_connection()
    try:
        if conn:
            create_tables(conn)

            # Populate tables (Task 3)
            p1 = add_publisher(conn, "TechMedia")
            p2 = add_publisher(conn, "HealthWorld")
            p3 = add_publisher(conn, "DailyNews")

            m1 = add_magazine(conn, "Tech Today", p1)
            m2 = add_magazine(conn, "Health Digest", p2)
            m3 = add_magazine(conn, "Morning Herald", p3)

            s1 = add_subscriber(conn, "Alice Smith", "123 Main St")
            s2 = add_subscriber(conn, "Bob Johnson", "456 Elm St")
            s3 = add_subscriber(conn, "Charlie Lee", "789 Oak St")

            add_subscription(conn, s1, m1, "2025-12-31")
            add_subscription(conn, s1, m2, "2025-11-30")
            add_subscription(conn, s2, m3, "2026-01-15")
            add_subscription(conn, s3, m1, "2025-10-01")
            add_subscription(conn, s3, m2, "2025-08-20")

            # Run queries (Task 4)
            get_all_subscribers(conn)
            get_all_magazines_sorted(conn)
            get_magazines_by_publisher(conn, "TechMedia")

    finally:
        if conn:
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main() 