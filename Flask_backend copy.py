from flask import Flask, request, jsonify
import sqlite3
import asyncio

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def insert_and_predict(data):
            conn = sqlite3.connect(
                r"C:\Users\Toshiba\Documents\PD2_john\databases\SensorReadings.db"
            )
            cursor = conn.cursor()
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
            conn.commit()
            from prediction import prediction
            result = await prediction(data, conn)
            conn.close()
            return result
        result = loop.run_until_complete(insert_and_predict(data))
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
