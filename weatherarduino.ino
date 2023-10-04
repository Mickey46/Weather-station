#include <Wire.h>
#include <DHT.h>

#define DHTPIN 3
#define SOIL_TEMP_PIN A0  // Analog pin for soil temperature probe
#define SOIL_MOISTURE_PIN 2  // Pin for soil moisture sensor
#define SOUND_SENSOR_PIN A1  // Analog pin for sound detection module
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000); // Wait for 2 seconds between measurements

  float humidity = dht.readHumidity();
  float airTemperatureCelsius = dht.readTemperature();
  if (isnan(airTemperatureCelsius)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  float airTemperatureFahrenheit = (airTemperatureCelsius * 9.0 / 5.0) + 32.0; // Convert Celsius to Fahrenheit
  float soilTemperatureCelsius = readSoilTemperature(); // Read soil temperature from the probe
  float soilTemperatureFahrenheit = (soilTemperatureCelsius * 9.0 / 5.0) + 32.0; // Convert Celsius to Fahrenheit
  int soilMoistureValue = analogRead(SOIL_MOISTURE_PIN);
  int soundLevel = analogRead(SOUND_SENSOR_PIN); // Read sound level from the sound sensor

  // Calculate wind speed based on sound level (adjust the mapping equation according to your sensor specifications)
  float windSpeed = map(soundLevel, 0, 1023, 0, 100); // Example mapping from 0 to 100 mph

  Serial.print("Air Temperature: ");
  Serial.print(airTemperatureFahrenheit);
  Serial.print(" °F, Humidity: ");
  Serial.print(humidity);
  Serial.print(" %, Soil Temperature: ");
  Serial.print(soilTemperatureFahrenheit);
  Serial.print(" °F, Soil Moisture: ");
  Serial.print(soilMoistureValue);
  Serial.print(", Wind Speed: ");
  Serial.print(windSpeed);
  Serial.println(" mph");

  delay(5000); // Wait for 5 seconds before the next set of readings
}

float readSoilTemperature() {
  int soilTemperatureValue = analogRead(SOIL_TEMP_PIN);
  // Convert analog value to voltage (0 to 5V)
  float voltage = soilTemperatureValue * (5.0 / 1023.0);
  // Convert voltage to temperature in degrees Celsius based on your sensor's specifications
  float temperatureCelsius = voltage * 100.0; // Example mapping for a certain probe
  return temperatureCelsius;
}
