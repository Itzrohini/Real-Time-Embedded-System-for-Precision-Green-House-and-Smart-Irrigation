import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import urllib.request
import pickle
from tensorflow.keras.models import load_model
from time import sleep
import os
# Load your pre-trained models (CNN for image, KNN for sensor data)
cnn_model = load_model('CNN.model')  # Replace with the correct path
knn_model = pickle.load(open('model1.sav', 'rb'))  # Load KNN model

base = "http://192.168.137.144/"
esp32_cam_url = "http://192.168.137.39/capture"  # ESP32-CAM URL

data_dir = "data"
# Update class labels accordingly
class_names = os.listdir(data_dir)
image_health_status = None  # Global variable to store image classification result

# Function to preview ESP32-CAM feed and capture on 'q' press
def preview_esp32cam():
    while True:
        try:
            img_resp = urllib.request.urlopen(esp32_cam_url)
            img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)

            if img is None:
                raise Exception("Failed to retrieve image.")

            cv2.imshow("ESP32-CAM Preview", img)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Capture image when 'q' is pressed
                cv2.destroyAllWindows()
                classify_image(img)
                break

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch image: {e}")
            break

# Function to classify the captured image
def classify_image(img):
    global image_health_status

    try:
        img = cv2.medianBlur(img, 1)
        img = cv2.resize(img, (50, 50))  # Adjust size if needed
        img = np.expand_dims(img, axis=0)
        img = img / 255.0  # Normalize

        # Predict using CNN
        predictions = cnn_model.predict(img)
        class_index = np.argmax(predictions)
        class_label = class_names[class_index]

        # Update UI
        result_label.config(text=f'Image Result: {class_label}')
        image_health_status = "healthy" if class_label.lower() == "healthy" else "unhealthy"

        # Get sensor data automatically after image classification
        get_sensor_data()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to classify image: {e}")

# Function to get sensor data and predict health

def get_sensor_data():
    global plant_health_percentage
    try:
        ct = 0
        res = transfer(str(ct))
        response = str(res)
        values = response.split('-')

        if len(values) == 5:
            v1, c1, ch, dh, additional_value = values
            reports = [[float(v1), float(c1), float(ch), float(dh), float(additional_value)]]

            # Predict using KNN model
            predicted = knn_model.predict(reports)
            plant_health_percentage = predicted[0]
            print(plant_health_percentage)

            # Update UI
            health_label.config(text=f'Crop: {plant_health_percentage}')
            send_to_cloud(v1, c1, ch, dh, additional_value, plant_health_percentage)

            # Check overall health

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch sensor data: {e}")

# Function to send data to ThingSpeak
def send_to_cloud(v1, c1, ch, dh, additional_value, health):
    try:
        conn = urllib.request.urlopen(
            f"https://api.thingspeak.com/update?api_key=GNRSRJK8C2GWOPAC&field1={v1}&field2={c1}&field3={ch}&field4={dh}&field5={additional_value}&field6={plant_health_percentage}"
        )
        conn.read()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send data to the cloud: {e}")

# Function to display a remedy based on plant health

# Function to check overall health by comparing CNN and KNN results


# Function to transfer sensor data
def transfer(my_url):
    try:
        response = urllib.request.urlopen(base + my_url).read().decode("utf-8")
        return response
    except Exception as e:
        return str(e)

# Create a tkinter window
root = tk.Tk()
root.title("Plant Health Classifier")

# Create a label for the title
title_label = tk.Label(root, text="Plant Health Classification", font=("Helvetica", 20))
title_label.pack(pady=20)

# Create a label to display the image classification result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Create a label to display the plant health percentage
health_label = tk.Label(root, text="", font=("Helvetica", 16))
health_label.pack(pady=20)

# Create a label to display the remedy


# Create a label to display the overall health

# Create a button to preview the ESP32-CAM feed and capture image on 'q' press
classify_button = tk.Button(root, text="Start Camera & Capture", command=preview_esp32cam)
classify_button.pack(pady=10)

# Create a quit button
quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(pady=10)

# Start the tkinter main loop
root.mainloop()