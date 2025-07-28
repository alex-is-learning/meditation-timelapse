import cv2
import time
import os

# --- Configuration ---
CAPTURE_INTERVAL = 300  # 300 seconds = 5 minutes
OUTPUT_DIR = "timelapse_images"
CAMERA_INDEX = 0

# --- Text Overlay Settings ---
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 4
FONT_COLOR = (255, 255, 255) # White color (B, G, R)
FONT_THICKNESS = 4
# Define separate positions for each line of text
ELAPSED_TEXT_POSITION = (20, 120) # (x, y) from top-left
TIMESTAMP_TEXT_POSITION = (20, 240)

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
        # --- DYNAMIC WAIT LOGIC ---
        # This section decides how long to wait before each capture.
        if image_count == 0:
            # For the first photo, wait 1 minute (60 seconds)
            wait_time_seconds = 60
            print("Waiting for 1 minute to take the first photo...")
        elif image_count == 1:
            # For the second photo, wait 4 minutes (240 seconds) to reach the 5-min mark
            wait_time_seconds = 240
            print("Waiting for 4 minutes for the next photo (at the 5-minute mark)...")
        else:
            # For all subsequent photos, wait the standard 5-minute interval
            wait_time_seconds = CAPTURE_INTERVAL
            interval_in_minutes = int(wait_time_seconds / 60)
            print(f"Waiting for {interval_in_minutes} minutes until the next capture...")

        time.sleep(wait_time_seconds)
        
        # --- CAPTURE AND PROCESS IMAGE ---
        ret, frame = cap.read()
        
        if ret:
            image_count += 1
            
            # 1. Calculate the correct elapsed time for the text overlay
            if image_count == 1:
                elapsed_minutes = 1
            else:
                # After the first shot, the time is 5 mins, 10 mins, 15 mins...
                interval_in_minutes = int(CAPTURE_INTERVAL / 60)
                elapsed_minutes = interval_in_minutes * (image_count - 1)
            
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
            
            print(f"[{image_count}] Captured {filename} at approx. {elapsed_minutes} minutes.")
            
        else:
            print("Failed to capture frame. Retrying in 5 seconds...")
            time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping time-lapse capture.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released. Exiting.")