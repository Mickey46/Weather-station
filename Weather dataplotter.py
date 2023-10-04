import serial
import re
import matplotlib.pyplot as plt
from collections import deque

# Establish a serial connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to match your Arduino's port and 9600 to match your Arduino's baud rate

# Initialize lists to store data
MAX_LENGTH = 50  # Maximum number of data points to display on the graph
timestamps = deque(maxlen=MAX_LENGTH)
temperature = deque(maxlen=MAX_LENGTH)
humidity = deque(maxlen=MAX_LENGTH)
soil_temperature = deque(maxlen=MAX_LENGTH)
soil_moisture = deque(maxlen=MAX_LENGTH)
wind_speed = deque(maxlen=MAX_LENGTH)

# Function to update the live plot
def update_plot():
    plt.clf()  # Clear the previous plot
    plt.subplot(2, 1, 1)
    plt.title('Temperature and Humidity')
    plt.grid(True)
    plt.ylabel('Temperature (°F)')
    plt.plot(timestamps, temperature, 'r-', label='Temperature')
    plt.plot(timestamps, humidity, 'b-', label='Humidity')
    plt.legend(loc='upper left')

    plt.subplot(2, 1, 2)
    plt.title('Soil Temperature, Soil Moisture, and Wind Speed')
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.plot(timestamps, soil_temperature, 'r-', label='Soil Temperature')
    plt.plot(timestamps, soil_moisture, 'b-', label='Soil Moisture')
    plt.plot(timestamps, wind_speed, 'g-', label='Wind Speed')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.pause(0.01)  # Pause to allow time for the plot to update

# Read data from Arduino and update lists
while True:
    arduino_data = ser.readline().decode().strip()
    if arduino_data:
        try:
            # Extract numerical values using regular expressions
            values = re.findall(r'[0-9.]+', arduino_data)
            if len(values) >= 5:
                air_temp = float(values[0])
                humidity_val = float(values[1])
                soil_temp = float(values[2])
                soil_moisture_val = float(values[3])
                wind_speed_val = float(values[4])

                # Append data to lists
                timestamps.append(timestamps[-1] + 1 if timestamps else 1)  # Incrementing timestamp for each data point
                temperature.append(air_temp)
                humidity.append(humidity_val)
                soil_temperature.append(soil_temp)
                soil_moisture.append(soil_moisture_val)
                wind_speed.append(wind_speed_val)

                # Update the live plot
                update_plot()

        except (ValueError, IndexError) as e:
            print(f"Error parsing data: {e}")

