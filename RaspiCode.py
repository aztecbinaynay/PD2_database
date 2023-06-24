import random
import string
from datetime import datetime, timedelta
import requests

# Generate a random 6-digit userID using letters and digits
userID = "Beb123"

# Define the start time and end time for TimeIn and TimeOut
start_time = datetime(2023, 6, 20, 8, 0, 0)
end_time = start_time + timedelta(hours=8)

# num_data_points = 172800

# Convert lists to strings
print("Data being made into strings")

file_path = r"C:\Users\Toshiba\Documents\PD2_john\databases\data_1687589315209.txt"

result = {}

with open(file_path, "r") as file:
    lines = file.readlines()

header = lines[0].strip().split("\t")  # Get the column names from the first line

for i in range(len(header)):
    column_values = [
        float(row.strip().split("\t")[i]) for row in lines[1:]
    ]  # Convert values to floats
    result[header[i]] = column_values

therm_data = str(result["DHT11"])
ecg_data = str(result["ECG"])
airflow_data = str(result["AirFlow"])
snore_data = str(result["Snore"])
spo2_data = str(result["SpO2"])
hr_data = str(result["PulseRate"])

# Create the dictionary with keys and values
print("Data being created")
data_dict = {
    "UserID": userID,
    "Therm": therm_data,
    "ECG": ecg_data,
    "Airflow": airflow_data,
    "Snore": snore_data,
    "SpO2": spo2_data,
    "HR": hr_data,
    "TimeIn": start_time.strftime("%Y-%m-%d %H:%M:%S"),
    "TimeOut": end_time.strftime("%Y-%m-%d %H:%M:%S"),
}
print("Data created")

url = "http://localhost:5000/insert"

# Send the request and measure the time taken
print("Sending request...")
start = datetime.now()
response = requests.post(url, json=data_dict)
end = datetime.now()
duration = end - start
print("Request completed in", duration.total_seconds(), "seconds")

print(response.status_code, response.reason, response.text)
