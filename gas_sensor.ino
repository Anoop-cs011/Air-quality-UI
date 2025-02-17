// SDA-->21
// SCL-->22
// VCC-->3v3
// GND-->GND
/* Operating voltage	3.3V/5V  (GSR) */

#include <Multichannel_Gas_GMXXX.h>
#include <Wire.h>
#define GSR_PIN 32 // Define the GPIO pin connected to the SIG pin of the GSR sensor
GAS_GMXXX<TwoWire> gas;

void setup() {
  Serial.begin(9600);
  pinMode(GSR_PIN, INPUT);
  Wire.begin(); // Initialize I2C communication
  gas.begin(Wire, 0x08); // Start the gas sensor with I2C address 0x08
}

void loop() {
  // Read sensor values
  int val_NO2 = gas.getGM102B();
  int val_C2H5CH = gas.getGM302B();
  int val_VOC = gas.getGM502B();
  int val_CO = gas.getGM702B();
  int sensorValue = analogRead(GSR_PIN);
  // Serial.print("...");
  Serial.print(val_NO2);
  Serial.print(",");
  Serial.print(val_C2H5CH);
  Serial.print(",");
  Serial.print(val_VOC);
  Serial.print(",");
  Serial.println(val_CO);


  delay(1000); // Adjust the delay as needed
}