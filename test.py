import cv2
import time
import os

# --- Test Configuration ---
NUM_PHOTOS = 2         # Total number of photos to take
INTERVAL = 1            # Interval in seconds
OUTPUT_DIR = "test_images"
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

print(f"Starting test: Taking {NUM_PHOTOS} photos, {INTERVAL} second apart...")

# --- Main Loop ---
try:
    for i in range(NUM_PHOTOS):
        # The loop counter 'i' goes from 0 to 9. We add 1 for display.
        image_count = i + 1
        
        ret, frame = cap.read()
        
        if ret:
            # 1. Generate elapsed seconds text
            elapsed_text = f"{image_count} sec"
            
            # 2. Generate full timestamp text
            timestamp_text = time.strftime("%Y-%m-%d %H:%M:%S")

            # 3. Draw both text strings on the frame
            cv2.putText(frame, elapsed_text, ELAPSED_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            cv2.putText(frame, timestamp_text, TIMESTAMP_TEXT_POSITION, FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            
            # Save the modified frame
            file_timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(OUTPUT_DIR, f"test_image_{file_timestamp}.jpg")
            cv2.imwrite(filename, frame)
            
            print(f"[{image_count}/{NUM_PHOTOS}] Captured {filename}")
            
            # Wait for the defined interval
            time.sleep(INTERVAL)
        else:
            print("Failed to capture frame.")
            break # Exit the loop if the camera fails

except KeyboardInterrupt:
    print("\nTest stopped by user.")

