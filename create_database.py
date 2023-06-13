import sqlite3

conn = sqlite3.connect(r'C:\Users\Toshiba\Documents\PD2_john\databases\SensorReadings.db')
cursor = conn.cursor()

# Create the SensorReadings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SensorReadings (
        ID INTEGER PRIMARY KEY,
        UserID INTEGER NOT NULL,
        Therm TEXT,
        ECG TEXT,
        Airflow TEXT,
        Snore TEXT,
        SpO2 TEXT,
        HR TEXT,
        TimeIn DATETIME,
        TimeOut DATETIME
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()