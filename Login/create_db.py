import os
import sqlite3

# Function to create the database and Property table if they don't exist
def create_db_and_table():
    conn = sqlite3.connect('props.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Property (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Key TEXT NOT NULL,
        Value TEXT NOT NULL,
        isActive INTEGER NOT NULL,
        PropertyType TEXT NOT NULL
    )
    ''')

    # Insert some initial data
    properties = [
        ('Home', 'Home.html', 1, 'File Path'),
        ('login', 'login.html', 1, 'File Path'),
        ('signin', 'signin.html', 1, 'File Path'),
        ('OTP', 'OTP.html', 1, 'File Path'),
        ('reset', 'reset.html', 1, 'File Path'),
        ('verify_otp', 'verify_otp.html', 1, 'File Path'),
        ('Home1', 'static/Home.css', 1, 'File Path'),
        ('login1', 'static/login.css', 1, 'File Path'),
        ('login2', 'static/login.js', 1, 'File Path'),
        ('OTP1', 'static/OTP.css', 1, 'File Path'),
        ('mail_password', 'izfp obyx bjrr xeys', 1, 'Mail Config'),
        ('mail_username', 'amritanshu05yadav@gmail.com', 1, 'Mail Config')
    ]

    for prop in properties:
        cursor.execute('''
        INSERT OR IGNORE INTO Property (Key, Value, isActive, PropertyType)
        VALUES (?, ?, ?, ?)
        ''', prop)

    conn.commit()
    conn.close()

# Function to add a new property to the Property table
def add_property(key, value, is_active, property_type):
    conn = sqlite3.connect('props.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO Property (Key, Value, isActive, PropertyType)
    VALUES (?, ?, ?, ?)
    ''', (key, value, is_active, property_type))
    conn.commit()
    conn.close()

# Main function
def main():
    # Get the path of the current script
    file_path = os.path.abspath(__file__)

    # Create the database and table if they don't exist
    create_db_and_table()

    # Add the file path of the current script to the Property table
    add_property('create_db_path', file_path, 1, 'File Path')

    print(f'File path {file_path} added to props.db.')

    # Fetch and print data from the Property table
    conn = sqlite3.connect('props.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Property')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
