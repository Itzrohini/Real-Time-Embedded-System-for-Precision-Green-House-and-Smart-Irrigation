#include <SoftwareSerial.h>
#include "ESP_Wahaj.h"
#include <LCD_I2C.h>

LCD_I2C lcd(0x27);
float ph;
#include <Adafruit_MCP3008.h>
#include <SimpleDHT.h>
int pinDHT11 = D0;
int t,h;
SimpleDHT11 dht11(pinDHT11);
Adafruit_MCP3008 adc;

int count = 0;
// Define the software serial object
SoftwareSerial mySerial(D3, D4); // D1 is RX, D2 is TX

void setup() {
  // Start serial communication
  Serial.begin(9600);
  start("Project","12345678");
  adc.begin();
  lcd.begin(); // If you are using more I2C devices using the Wire library use lcd.begin(false)
                 // this stop the library(LCD_I2C) from calling Wire.begin()
    lcd.backlight();
  // Start software serial communication
  mySerial.begin(9600);
  lcd.setCursor(0, 0);
   lcd.print("PLANT HEALTH"); // You can make spaces using well... spaces
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print("MONITOR");
    delay(2500);
    lcd.clear();
}

void loop() {
  if (CheckNewReq()==1) {
  // Check if data is available to read from software serial
  if (mySerial.available() > 0) {
    // Read the incoming data
    String incomingData = mySerial.readString();
    
    // Print the received data
    Serial.print("Received: ");
    Serial.println(incomingData);

    // Find the position of 'PH:'
    int phIndex = incomingData.indexOf("PH:");

    // If 'PH:' is found, extract the pH value
    if (phIndex != -1) {
      // Extract the substring starting from 'PH:' to the end
      String phValue = incomingData.substring(phIndex + 3);
      
      // Find the position of the next comma to isolate the pH value
      int commaIndex = phValue.indexOf(',');

      // If a comma is found, extract the pH value before the comma
      if (commaIndex != -1) {
        phValue = phValue.substring(0, commaIndex);
      }
      Serial.print("pH Value: ");
      ph=phValue.toFloat();
      Serial.println(ph);
       byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  t=temperature;
  h=humidity;
  Serial.print(t); Serial.print(" *C, "); 
  Serial.print(h); Serial.println(" H");
    }
  }
 
   int ra=adc.readADC(0);
   int rm=adc.readADC(1);
       lcd.setCursor(0, 0);
   lcd.print("T: "); // You can make spaces using well... spaces
   lcd.print(t);
   lcd.print(" H: "); // You can make spaces using well... spaces
   lcd.print(h);
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print("PH:");
    lcd.print(ph);
    delay(2500);
    lcd.clear();
          lcd.setCursor(0, 0);
   lcd.print("N: "); // You can make spaces using well... spaces
   lcd.print(ra);
    lcd.setCursor(0, 1); // Or setting the cursor in the desired position.
    lcd.print("MOI:");
    lcd.print(rm);
    delay(2500);
    lcd.clear();
      
      String myString = String(t)+String("-")+String(h)+String("-")+String(ph)+String("-")+String(ra)+String("-")+String(rm);
    returnThisStr(myString);
    delay(1000);
String path = getPath();  
  }
}
