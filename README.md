# 🌱 REAL TIME EMBEDDED SYSTEM FOR PRECISION GREENHOUSE AND SMART IRRIGATION

This project presents a **real-time embedded system** integrating **IoT sensors** and **AI-based plant disease detection** to enhance smart irrigation and greenhouse management.  
It continuously monitors environmental and soil parameters like **temperature, humidity, pH, and soil moisture**, and uses **CNN (Convolutional Neural Networks)** to detect plant leaf diseases.

---

##  DATASET & RESOURCES

-  **Leaf Image Dataset (ZIP):** [Download from Google Drive](https://drive.google.com/file/d/1yqRFZw-xMvbLoj4Yx1Tqa7uR9z3-PaIF/view?usp=sharing)
-  **Crop Dataset (CSV):** [View on GitHub](https://github.com/Itzrohini/Real-Time-Embedded-System-for-Precision-Green-House-and-Smart-Irrigation/blob/main/crop_dataset.csv)

---

##  PROJECT OVERVIEW

This system combines **Embedded IoT Hardware** with **Deep Learning** to achieve:
-  Real-time monitoring of greenhouse parameters  
-  CNN-based plant disease prediction  
-  Automated irrigation based on soil conditions  
-  LCD display showing live sensor readings  
-  Integration of temperature, humidity, pH, and soil moisture sensors  

---

## TECHNOLOGIES USED

| Component | Description |
|------------|-------------|
|  Python | Data processing & CNN training |
|  TensorFlow / Keras | Deep learning model |
|  Arduino / ESP8266 | IoT hardware platform |
|  DHT11 Sensor | Temperature & humidity monitoring |
|  pH & Soil Sensors | Soil health monitoring |
|  LCD (I2C) | Real-time display |
|  SoftwareSerial / WiFi | Data communication |

---

---

## 📂 Folder Structure

```plaintext
Real-Time-Embedded-System-for-Precision-Green-House-and-Smart-Irrigation/
│
├── 📁 CNN_Model/
│   ├── train.py
│   ├── test.py
│   ├── model.h5
│   ├── requirements.txt
│
├── 📁 Arduino_Code/
│   ├── main.ino
│   ├── ESP_Wahaj.h
│   ├── LCD_I2C.h
│
├── 📁 Dataset/
│   ├── crop_dataset.csv
│   └── Leaf_Image_Dataset.zip (Google Drive)
│
├── 📁 Results/
│   ├── output_sample1.png
│   ├── lcd_display.png
│
└── README.md
---

###  How to Run (Python + IoT)

###  Python / CNN Model

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
Download the dataset from Google Drive:
Leaf Image Dataset (Google Drive)

Place the downloaded dataset inside the Dataset/ folder.

Train the CNN model

bash
Copy code
python train.py
Once training is complete, a file named model.h5 will be generated automatically.

Test the model

bash
Copy code
python test.py
 IoT / Arduino Setup
Open main.ino inside the Arduino_Code/ folder using Arduino IDE.

Connect your NodeMCU / ESP8266 board.

Install the following libraries (via Library Manager or manually):

SoftwareSerial.h

Adafruit_MCP3008.h

SimpleDHT.h

LCD_I2C.h

ESP_Wahaj.h

Select the correct Board and COM Port:

scss
Copy code
Tools → Board → NodeMCU 1.0 (ESP-12E Module)
Tools → Port → [Your Port]
Click Upload to flash the code to your board.

Open Serial Monitor at 9600 baud rate to see live readings of:

Temperature

Humidity

pH value

Soil moisture

The LCD will display real-time values, and data will be sent to the web or Power BI dashboard for visualization.






