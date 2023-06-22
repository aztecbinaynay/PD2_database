import random
import string
from datetime import datetime, timedelta
import requests

# Generate a random 6-digit userID using letters and digits
userID = "XYZ691"

# Define the start time and end time for TimeIn and TimeOut
start_time = datetime(2023, 6, 20, 8, 0, 0)
end_time = start_time + timedelta(hours=8)

num_data_points = 165963

# Convert lists to strings
print("Data being made into strings")

therm_data = str([random.randint(0, 500) for _ in range(num_data_points)])
ecg_data = str([random.randint(0, 500) for _ in range(num_data_points)])
airflow_data = str([random.randint(0, 500) for _ in range(num_data_points)])
snore_data = str([random.randint(0, 500) for _ in range(num_data_points)])
spo2_data = str([random.randint(0, 500) for _ in range(num_data_points)])
hr_data = str([random.randint(0, 500) for _ in range(num_data_points)])

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
