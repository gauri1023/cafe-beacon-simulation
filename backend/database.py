import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cafe.db')

def get_db_connection():
    """Create and return a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed initial data if not already present."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create table for Café details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cafe_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tagline TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            opening_hours TEXT,
            description TEXT
        )
    ''')

    # 2. Create table for Beacons
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beacons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beacon_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            range_meters INTEGER DEFAULT 10,
            status TEXT DEFAULT 'active'
        )
    ''')

    # 3. Create table for Offers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beacon_id TEXT NOT NULL,
            title TEXT NOT NULL,
            discount TEXT NOT NULL,
            item TEXT NOT NULL,
            promo_code TEXT,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (beacon_id) REFERENCES beacons (beacon_id)
        )
    ''')

    # Seed Café details if table is empty
    cursor.execute('SELECT COUNT(*) FROM cafe_details')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO cafe_details (name, tagline, address, phone, email, opening_hours, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Beacon Brew Café',
            'Walk in. Your coffee deal finds you.',
            '12 Coffee Lane, University Campus',
            '+91 98765 43210',
            'hello@beaconbrew.cafe',
            '08:00 AM - 10:00 PM',
            'Beacon Brew is a café that greets you the moment you get close with proximity beacon technology.'
        ))

    # Seed Beacon CAFE001 if not present
    cursor.execute('SELECT COUNT(*) FROM beacons WHERE beacon_id = ?', ('CAFE001',))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO beacons (beacon_id, name, location, range_meters, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'CAFE001',
            'Main Entrance Beacon',
            'Café Front Entrance',
            10,
            'active'
        ))

    # Seed Offer: 20% OFF on coffee for CAFE001 if not present
    cursor.execute('SELECT COUNT(*) FROM offers WHERE beacon_id = ?', ('CAFE001',))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO offers (beacon_id, title, discount, item, promo_code, description, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'CAFE001',
            'Welcome! Get 20% OFF on Coffee!',
            '20% OFF',
            'Coffee',
            'BEACON20',
            '20% OFF on any coffee for customers within 10 m.',
            1
        ))

    conn.commit()
    conn.close()

def get_cafe_details():
    """Retrieve café details."""
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM cafe_details ORDER BY id ASC LIMIT 1').fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_beacon_by_id(beacon_id):
    """Retrieve beacon details by beacon ID."""
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM beacons WHERE beacon_id = ?', (beacon_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_beacons():
    """Retrieve all registered beacons."""
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM beacons').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_offer_by_beacon(beacon_id):
    """Retrieve active offer associated with a specific beacon ID."""
    conn = get_db_connection()
    query = '''
        SELECT o.*, b.name as beacon_name, b.location as beacon_location, b.range_meters
        FROM offers o
        JOIN beacons b ON o.beacon_id = b.beacon_id
        WHERE o.beacon_id = ? AND o.is_active = 1
        ORDER BY o.id DESC
        LIMIT 1
    '''
    row = conn.execute(query, (beacon_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_offers():
    """Retrieve all offers."""
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM offers').fetchall()
    conn.close()
    return [dict(r) for r in rows]
