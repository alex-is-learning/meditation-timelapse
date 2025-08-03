import cv2
import time
import os
import random

def prompt_user():
    print("Welcome to Meditation Timelapse!")
    while True:
        try:
            interval = float(input("How often would you like to take a photo? (seconds): "))
            if interval <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            setup_delay = int(input("How many seconds would you like to set up before the first photo? (e.g., 60): "))
            if setup_delay < 0:
                print("Please enter zero or a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    mode = input("Do you want to take photos for a limited number of photos (p), seconds (s), or indefinitely (i)? [p/s/i]: ").strip().lower()
    if mode == 'p':
        while True:
            try:
                num_photos = int(input("How many photos?: "))
                if num_photos <= 0:
                    print("Please enter a positive integer.")
                    continue
                return interval, setup_delay, 'photos', num_photos
            except ValueError:
                print("Please enter a valid integer.")
    elif mode == 's':
        while True:
            try:
                total_seconds = int(input("How many seconds total?: "))
                if total_seconds <= 0:
                    print("Please enter a positive integer.")
                    continue
                return interval, setup_delay, 'seconds', total_seconds
            except ValueError:
                print("Please enter a valid integer.")
    else:
        return interval, setup_delay, 'infinite', None

# --- Text Overlay Settings ---
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255) # White
BG_COLOR = (0, 0, 0)         # Black
PADDING = 5                  # Pixels of padding inside the black bars
PRIMARY_FONT_SCALE = 2
PRIMARY_FONT_THICKNESS = 3
JOKE_FONT_SCALE = 1.2
JOKE_FONT_THICKNESS = 2
START_X = 20
START_Y = 40
LINE_GAP = 10

# --- Helper Function ---
def draw_text_with_bg(frame, text, top_left_position, font, scale, text_color, bg_color, thickness, padding=PADDING):
    x, y = top_left_position
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    bar_end = (x + text_width + padding * 2, y + text_height + baseline + padding * 2)
    cv2.rectangle(frame, (x, y), bar_end, bg_color, -1)
    text_baseline_y = y + text_height + padding + (baseline // 2)
    text_position = (x + padding, text_baseline_y)
    cv2.putText(frame, text, text_position, font, scale, text_color, thickness)
    return bar_end[1] - y

# --- Main ---
def main():
    interval, setup_delay, mode, limit = prompt_user()
    print("\nREMINDER: Before you begin...")
    print("- Set a timer for your meditation session (on your phone or device).")
    print("- Enable Do Not Disturb mode to avoid interruptions.")
    input("\nPress Enter when you are ready to continue...")
    OUTPUT_DIR = "timelapse_images"
    CAMERA_INDEX = 0
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise IOError(f"Cannot open webcam with index {CAMERA_INDEX}")
    samsara_cycles_this_session = random.randint(999999, 99999999)
    print("Starting time-lapse. Press Ctrl+C to stop.")
    image_count = 0
    start_time = time.time()
    try:
        if setup_delay > 0:
            print(f"Waiting {setup_delay} seconds for you to set up before the first photo...")
            time.sleep(setup_delay)
        while True:
            now = time.time()
            if mode == 'photos' and image_count >= limit:
                print("Reached requested number of photos.")
                break
            if mode == 'seconds' and (now - start_time) >= limit:
                print("Reached requested duration.")
                break
            ret, frame = cap.read()
            if ret:
                image_count += 1
                elapsed_seconds = int(now - start_time)
                elapsed_minutes = elapsed_seconds // 60
                minutes_text = f"{elapsed_minutes} min" if elapsed_minutes == 1 else f"{elapsed_minutes} mins"
                timestamp_text = time.strftime("%Y-%m-%d %H:%M:%S")
                # Draw only minutes and date
                current_y = START_Y
                for text, scale, thickness in [
                    (minutes_text, PRIMARY_FONT_SCALE, PRIMARY_FONT_THICKNESS),
                    (timestamp_text, PRIMARY_FONT_SCALE, PRIMARY_FONT_THICKNESS)
                ]:
                    bar_height = draw_text_with_bg(frame, text, (START_X, current_y), FONT, scale, FONT_COLOR, BG_COLOR, thickness)
                    current_y += bar_height + LINE_GAP
                filename = os.path.join(OUTPUT_DIR, f"image_{time.strftime('%Y%m%d-%H%M%S')}.jpg")
                cv2.imwrite(filename, frame)
                print(f"[{image_count}] Captured {filename} at {minutes_text}.")
                # Sound playback removed due to stability issues
            else:
                print("Failed to capture frame. Retrying in 5 seconds...")
                time.sleep(5)
                continue
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopping time-lapse capture.")
    finally:
        # Sound playback removed due to stability issues
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam released. Exiting.")

if __name__ == "__main__":
    main()
