import cv2
import time
import os
import random

# --- Configuration ---
CAPTURE_INTERVAL = 300  # 300 seconds = 5 minutes
OUTPUT_DIR = "timelapse_images"
CAMERA_INDEX = 0

# --- Text Overlay Settings ---
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255) # White
BG_COLOR = (0, 0, 0)         # Black
PADDING = 5                  # Pixels of padding inside the black bars

# Font Styles
PRIMARY_FONT_SCALE = 3
PRIMARY_FONT_THICKNESS = 3
JOKE_FONT_SCALE = 1.5
JOKE_FONT_THICKNESS = 2

# Layout Controls
START_X = 20
START_Y = 40          # Y-position for the TOP of the first bar
LINE_GAP = 10         # The visible gap between each black bar

# --- Helper Function (Revised for Centring) ---
def draw_text_with_bg(frame, text, top_left_position, font, scale, text_color, bg_color, thickness):
    """Draws text with a background bar, properly centred on the Y-axis."""
    x, y = top_left_position
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)

    # Calculate bar size and draw it
    bar_end = (x + text_width + PADDING * 2, y + text_height + baseline + PADDING * 2)
    cv2.rectangle(frame, (x, y), bar_end, bg_color, -1)

    # **FIXED**: Calculate text position to be vertically centred inside the bar.
    text_baseline_y = y + text_height + PADDING + (baseline // 2)
    text_position = (x + PADDING, text_baseline_y)
    cv2.putText(frame, text, text_position, font, scale, text_color, thickness)

    # Return the total height of the bar just drawn
    return bar_end[1] - y

# --- Setup ---
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise IOError(f"Cannot open webcam with index {CAMERA_INDEX}")

# --- Pre-Loop Setup ---
samsara_cycles_this_session = random.randint(999999, 99999999)
print("Starting time-lapse. Press Ctrl+C to stop.")
image_count = 0

# --- Main Loop ---
try:
    while True:
        # --- DYNAMIC WAIT LOGIC ---
        if image_count == 0:
            wait_time_seconds = 1
            print("Waiting for 1 second to take the first photo...")
        elif image_count == 1:
            wait_time_seconds = 59
            print("Waiting for 59 seconds for the next photo (at the 1-minute mark)...")
        elif image_count == 2:
            wait_time_seconds = 240
            print("Waiting for 4 minutes for the next photo (at the 5-minute mark)...")
        else:
            wait_time_seconds = CAPTURE_INTERVAL
            print(f"Waiting for 5 minutes until the next capture...")

        time.sleep(wait_time_seconds)
        
        # --- CAPTURE AND PROCESS IMAGE ---
        ret, frame = cap.read()
        if ret:
            image_count += 1
            
            # 1. Generate all text strings
            if image_count == 1: elapsed_text = "1 sec"
            elif image_count == 2: elapsed_text = "1 min"
            else: elapsed_text = f"{5 * (image_count - 2)} mins"

            text_lines = [
                (elapsed_text, PRIMARY_FONT_SCALE, PRIMARY_FONT_THICKNESS),
                (time.strftime("%Y-%m-%d %H:%M:%S"), PRIMARY_FONT_SCALE, PRIMARY_FONT_THICKNESS),
                (f"Samsara Cycles Left: {samsara_cycles_this_session}", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS),
                (f"Concentration: {int(random.triangular(0, 100, 15))}%", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS),
                (f"Dukkha (Stress): {random.randint(20, 80)}%", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS),
                (f"Moha (Delusion): {random.randint(40, 95)}%", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS),
                (f"Tanha (Grasping): {random.randint(10, 70)}%", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS),
                (f"Dosa (Aversion): {random.randint(10, 70)}%", JOKE_FONT_SCALE, JOKE_FONT_THICKNESS)
            ]

            # 2. Draw text lines procedurally
            current_y = START_Y
            for text, scale, thickness in text_lines:
                bar_height = draw_text_with_bg(frame, text, (START_X, current_y), FONT, scale, FONT_COLOR, BG_COLOR, thickness)
                current_y += bar_height + LINE_GAP
            
            # 3. Save the modified frame
            filename = os.path.join(OUTPUT_DIR, f"image_{time.strftime('%Y%m%d-%H%M%S')}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[{image_count}] Captured {filename} at approx. {elapsed_text}.")
            
        else:
            print("Failed to capture frame. Retrying in 5 seconds...")
            time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping time-lapse capture.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released. Exiting.")