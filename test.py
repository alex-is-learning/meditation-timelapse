import cv2
import time
import os
import random

# --- Test Configuration ---
NUM_PHOTOS = 3
INTERVAL = 1
OUTPUT_DIR = "test_images"
CAMERA_INDEX = 0

# --- Text Overlay Settings ---
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255) # White
BG_COLOR = (0, 0, 0)         # Black

# Primary Text
PRIMARY_FONT_SCALE = 2
PRIMARY_FONT_THICKNESS = 3
ELAPSED_TEXT_POSITION = (20, 100)  # Moved down
TIMESTAMP_TEXT_POSITION = (20, 200) # Moved down

# Joke Text
JOKE_FONT_SCALE = 1.2
JOKE_FONT_THICKNESS = 2
JOKE_TEXT_START_Y = 280          # Moved down
JOKE_LINE_SPACING = 60           # Increased spacing

# --- Helper Function ---
def draw_text_with_bg(frame, text, position, font, scale, text_color, bg_color, thickness, padding=3):
    """Draws text with a background rectangle for better legibility."""
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    x, y = position  # This is the bottom-left corner of the text

    # Calculate rectangle coordinates with padding
    rect_start = (x - padding, y - text_height - baseline - padding)
    rect_end = (x + text_width + padding, y + baseline + padding)
    
    cv2.rectangle(frame, rect_start, rect_end, bg_color, -1)
    cv2.putText(frame, text, position, font, scale, text_color, thickness)

# --- Setup ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise IOError(f"Cannot open webcam with index {CAMERA_INDEX}")

# --- Pre-Loop Setup ---
samsara_cycles_this_session = random.randint(999999, 99999999)

print(f"Starting session: Taking {NUM_PHOTOS} photos, {INTERVAL} second apart...")
print(f"This session's remaining Samsara Cycles: {samsara_cycles_this_session}")

# --- Main Loop ---
try:
    start_time = time.time()
    for i in range(NUM_PHOTOS):
        image_count = i + 1
        
        ret, frame = cap.read()
        
        if ret:
            # 1. Generate text strings
            elapsed_seconds = int(time.time() - start_time)
            elapsed_text = f"Time Elapsed: {elapsed_seconds}s"
            timestamp_text = time.strftime("%Y-%m-%d %H:%M:%S")
            samsara_text = f"Samsara Cycles Left: {samsara_cycles_this_session}"
            concentration_value = int(random.triangular(0, 100, 15))
            concentration_text = f"Concentration: {concentration_value}%"
            dukkha_text = f"Dukkha (Stress): {random.randint(20, 80)}%"
            moha_text = f"Moha (Delusion): {random.randint(40, 95)}%"
            tanha_text = f"Tanha (Grasping): {random.randint(10, 70)}%"
            dosa_text = f"Dosa (Aversion): {random.randint(10, 70)}%"
            
            # 2. Draw all text using the helper function
            draw_text_with_bg(frame, elapsed_text, ELAPSED_TEXT_POSITION, FONT, PRIMARY_FONT_SCALE, FONT_COLOR, BG_COLOR, PRIMARY_FONT_THICKNESS)
            draw_text_with_bg(frame, timestamp_text, TIMESTAMP_TEXT_POSITION, FONT, PRIMARY_FONT_SCALE, FONT_COLOR, BG_COLOR, PRIMARY_FONT_THICKNESS)
            
            # Joke info
            joke_y = JOKE_TEXT_START_Y
            draw_text_with_bg(frame, samsara_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)
            joke_y += JOKE_LINE_SPACING
            draw_text_with_bg(frame, concentration_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)
            joke_y += JOKE_LINE_SPACING
            draw_text_with_bg(frame, dukkha_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)
            joke_y += JOKE_LINE_SPACING
            draw_text_with_bg(frame, moha_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)
            joke_y += JOKE_LINE_SPACING
            draw_text_with_bg(frame, tanha_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)
            joke_y += JOKE_LINE_SPACING
            draw_text_with_bg(frame, dosa_text, (20, joke_y), FONT, JOKE_FONT_SCALE, FONT_COLOR, BG_COLOR, JOKE_FONT_THICKNESS)

            # 3. Save the modified frame
            file_timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(OUTPUT_DIR, f"meditation_log_{file_timestamp}.jpg")
            cv2.imwrite(filename, frame)
            
            print(f"[{image_count}/{NUM_PHOTOS}] Captured {filename}")
            
            time.sleep(max(0, INTERVAL - (time.time() - start_time) % INTERVAL))
        else:
            print("Failed to capture frame.")
            break

except KeyboardInterrupt:
    print("\nSession stopped by user.")

finally:
    # --- Cleanup ---
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released.")
