from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()  # Get the JSON data from the request

    # Process the data as needed
    print(data)
    return "Data received and processed"


@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()  # Get the JSON data from the request
        conn = sqlite3.connect(
            r"C:\Users\Toshiba\Documents\PD2_john\databases\SensorReadings.db"
        )
        cursor = conn.cursor()

        # Begin a transaction
        conn.execute("BEGIN TRANSACTION")

        cursor.execute(
            """
            INSERT INTO SensorReadings (UserID, Therm, ECG, Airflow, Snore, SpO2, HR, TimeIn, TimeOut)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data["UserID"],
                data["Therm"],
                data["ECG"],
                data["Airflow"],
                data["Snore"],
                data["SpO2"],
                data["HR"],
                data["TimeIn"],
                data["TimeOut"],
            ),
        )

        # Commit the transaction if all insertions are successful
        conn.commit()
        conn.close()
        print("Data inserted")
        return "Data inserted"
    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        conn.close()
        print("Error", e)
        return "Data not inserted"


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
