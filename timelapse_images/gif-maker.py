from PIL import Image
import glob
import time

# --- Configuration ---
# Duration of each frame in the GIF, in milliseconds.
# 1000ms = 1 second. 200ms is a good speed for a 10-frame test.
FRAME_DURATION_MS = 200 
OUTPUT_FILENAME = "output_timelapse.gif"

# --- Main Script ---
# Generate a timestamp for the output filename
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_filename = f"output_timelapse_{timestamp}.gif"

print("Searching for .jpg files in this directory...")

# Find all files ending with .jpg and sort them.
# The sorting works because your filenames have timestamps.
filenames = sorted(glob.glob('*.jpg'))

if not filenames:
    print("❌ No .jpg files found. Please place this script in the folder with your images.")
else:
    print(f"Found {len(filenames)} images. Creating GIF...")
    
    # Open all images and store them in a list
    images = [Image.open(f) for f in filenames]
    
    # The first image is the base
    first_image = images[0]
    
    # Save the first image as a GIF, and append the rest
    first_image.save(
        OUTPUT_FILENAME,
        save_all=True,
        append_images=images[1:], # Append all images after the first one
        optimize=False,
        duration=FRAME_DURATION_MS,
        loop=0 # 0 means the GIF will loop indefinitely
    )
    
    print(f"✨ Success! GIF created: {OUTPUT_FILENAME}")

