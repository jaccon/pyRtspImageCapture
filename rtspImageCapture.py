import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

import cv2
import time

rtsp_url = "rtsp://admin:jaccon123456@192.168.1.23:554/onvif1"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

image_folder = 'screenshots/'
interval_seconds = 5
last_capture_time = time.time()

jpeg_quality = 90  # Adjust this value to control the image quality (0-100)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    current_time = time.time()
    if current_time - last_capture_time >= interval_seconds:
        
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        folderWrite = image_folder+str(time.strftime('%Y-%m-%d'))
        
        if os.path.exists(folderWrite):
            print(timestamp)
        else:
            print(f"Failed to create directory '{folderWrite}'.")
            os.makedirs(folderWrite)
        
        image_path = os.path.join(folderWrite, f'image_{timestamp}.jpg')  # Use .jpg extension
        cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        last_capture_time = current_time
        print(f'Image captured and saved: {image_path}')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
