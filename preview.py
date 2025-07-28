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
ELAPSED_TEXT_POSITION = (20, 120)
TIMESTAMP_TEXT_POSITION = (20, 240)

# --- Setup ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise IOError(f"Cannot open webcam with index {CAMERA_INDEX}")

# --- NEW: Live Preview for Framing 📸 ---
print("Starting live preview. Frame your shot, then press 'Q' to start the timelapse.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame for preview.")
        break
    
    # Display the resulting frame in a window
    cv2.imshow('Live Preview - Press Q to Start Timelapse', frame)
    
    # Wait for the 'q' key to be pressed to exit the preview
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Destroy the preview window before starting the main loop
cv2.destroyAllWindows()
print("Framing complete. Starting time-lapse sequence...")
# --- END of new section ---


# --- Main Loop ---
image_count = 0
try:
    while True:
        # --- DYNAMIC WAIT LOGIC ---
        if image_count == 0:
            wait_time_seconds = 60
            print("Waiting for 1 minute to take the first photo...")
        elif image_count == 1:
            wait_time_seconds = 240
            print("Waiting for 4 minutes for the next photo (at the 5-minute mark)...")
        else:
            wait_time_seconds = CAPTURE_INTERVAL
            interval_in_minutes = int(wait_time_seconds / 60)
            print(f"Waiting for {interval_in_minutes} minutes until the next capture...")

        time.sleep(wait_time_seconds)
        
        # --- CAPTURE AND PROCESS IMAGE ---
        ret, frame = cap.read()
        
        if ret:
            image_count += 1
            
            if image_count == 1:
                elapsed_minutes = 1
            else:
                interval_in_minutes = int(CAPTURE_INTERVAL / 60)
                elapsed_minutes = interval_in_minutes * (image_count - 1)
            
            elapsed_text = f"{elapsed_minutes} mins"
            timestamp_text = time.strftime("%Y-%m-%d %H:%M:%S")

            cv2.putText(frame, elapsed_text, ELAPSED_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            cv2.putText(frame, timestamp_text, TIMESTAMP_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            
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