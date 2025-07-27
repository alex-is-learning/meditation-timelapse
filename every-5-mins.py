import cv2
import time
import os

# --- Configuration ---
CAPTURE_INTERVAL = 300  # 300 seconds = 5 minutes
OUTPUT_DIR = "timelapse_images"
CAMERA_INDEX = 0

# --- Text Overlay Settings ---
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_COLOR = (255, 255, 255) # White color (B, G, R)
FONT_THICKNESS = 2
# Define separate positions for each line of text
ELAPSED_TEXT_POSITION = (20, 40) # (x, y) from top-left
TIMESTAMP_TEXT_POSITION = (20, 70) # Placed 30 pixels below the first line

# --- Setup ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise IOError(f"Cannot open webcam with index {CAMERA_INDEX}")

print("Starting time-lapse. Press Ctrl+C to stop.")
image_count = 0

# --- Main Loop ---
try:
    while True:
        print(f"Waiting for {int(CAPTURE_INTERVAL/60)} minutes until the next capture...")
        time.sleep(CAPTURE_INTERVAL)

        ret, frame = cap.read()
        
        if ret:
            image_count += 1
            
            # 1. Generate the elapsed minutes text
            interval_in_minutes = int(CAPTURE_INTERVAL / 60)
            elapsed_minutes = image_count * interval_in_minutes
            elapsed_text = f"{elapsed_minutes} mins"
            
            # 2. Generate the full timestamp text
            timestamp_text = time.strftime("%Y-%m-%d %H:%M:%S")

            # 3. Draw both text strings on the frame
            cv2.putText(frame, elapsed_text, ELAPSED_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            cv2.putText(frame, timestamp_text, TIMESTAMP_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            
            # Define the filename and save the modified frame
            file_timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(OUTPUT_DIR, f"image_{file_timestamp}.jpg")
            cv2.imwrite(filename, frame)
            
            print(f"[{image_count}] Captured {filename} with text: '{elapsed_text}'")
        else:
            print("Failed to capture frame. Retrying...")
            time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping time-lapse capture.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released. Exiting.")
