import subprocess
import time
import re
import cv2
import RPi.GPIO as GPIO

led_pin=40
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)


# Replace these paths with the actual paths to your files
weights_path = '/home/linga/yolov5/yolov5s.pt'
project_path = '/home/linga'
name = 'output'

# Camera configuration
source_path = 1  # Use the camera index or camera name if needed
capture_interval = 10  # Capture an image every 1 minute (60 seconds)

def capture_images():
    while True:
        # Open the camera
        camera = cv2.VideoCapture(source_path)
    
        # Check if the camera is opened correctly
        if not camera.isOpened():
            print("Error: Unable to access the camera.")
            return
        print("captured")
        
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(2)  # Wait for 1 second

        # Turn off the LED
        GPIO.output(led_pin, GPIO.LOW)
       
    
        # Set the resolution (optional, change it according to your needs)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        
        # Save the captured frame as an image file
        cv2.imwrite("/home/linga/captured_pic.jpeg", frame)
        
        # Release the camera
        camera.release()

        # Construct the command to run the detect.py script
        command = [
            'python',
            '/home/linga/yolov5/detect.py',
            '--weights', weights_path,
            '--source', '/home/linga/captured_pic.jpeg',
            '--save-txt',
            '--project', project_path,
            '--name', name
        ]

        # Run the detect.py script using subprocess.run()
        output_bytes = subprocess.check_output(command)

# Convert the bytes to a string
        output_str = output_bytes.decode('utf-8')

# Use regular expression to extract the class names from the output string
        match = re.search(r"Detected Class Names: \[(.*?)\]", output_str)

        if match:
            detected_class_names_str = match.group(1)
            detected_class_names = detected_class_names_str.split(', ')
            print("Detected Class Names:", detected_class_names)
        else:
            print("No class names found in the output.")

        # Sleep for the specified interval (1 minute) before capturing the next image
        time.sleep(capture_interval)
        

if __name__ == '__main__':
    capture_images()
    



