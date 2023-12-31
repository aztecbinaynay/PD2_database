from flask import Flask, request, jsonify
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


@app.route("/retrieve", methods=["POST"])
def get_data():
    try:
        data = request.get_json()  # Get the JSON data from the request
        conn = sqlite3.connect(
            r"C:\Users\Toshiba\Documents\PD2_john\databases\SensorReadings.db"
        )
        cursor = conn.cursor()

        # Begin a transaction
        conn.execute("BEGIN TRANSACTION")

        cursor.execute("SELECT * FROM SensorReadings WHERE UserID=?", (data["UserID"],))

        # Fetch the row from the result
        row = cursor.fetchone()

        if row is not None:
            # Extract the values from the row
            id_, UserID, Therm, ECG, Airflow, Snore, SpO2, HR, TimeIn, TimeOut = row

            # Create a dictionary to store the retrieved data
            data_dict2 = {
                "UserID": UserID,
                "Therm": Therm,
                "ECG": ECG,
                "Airflow": Airflow,
                "Snore": Snore,
                "SpO2": SpO2,
                "HR": HR,
                "TimeIn": TimeIn,
                "TimeOut": TimeOut,
            }
            conn.commit()
            conn.close()
            print("Data retrieved")
            return jsonify(data_dict2), 200

        conn.commit()
        conn.close()
        print("Data unavailable")
        return "row does not exist", 404

    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        conn.close()
        print("Error", e)
        return str(e), 500


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
