from PIL import Image
import glob
import time
import os

# --- Configuration ---
FRAME_DURATION_MS = 200
# Add a new configuration section for resizing
RESIZE_WIDTH = 960 # Set the desired width in pixels

# --- Main Script ---
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_filename = f"output_timelapse_{timestamp}.gif"

print(f"Searching for .jpg files in this directory...")
filenames = sorted(glob.glob('*.jpg'))

if not filenames:
    print("❌ No .jpg files found. Please place this script in the folder with your images.")
else:
    print(f"Found {len(filenames)} images. Creating GIF...")
    
    images = []
    print(f"Resizing images to a width of {RESIZE_WIDTH}px...")
    for f in filenames:
        img = Image.open(f)
        # Calculate new height to maintain the original aspect ratio
        aspect_ratio = float(img.size[1]) / float(img.size[0])
        new_height = int(aspect_ratio * RESIZE_WIDTH)
        # Resize the image using a high-quality filter
        img_resized = img.resize((RESIZE_WIDTH, new_height), Image.Resampling.LANCZOS)
        images.append(img_resized)
    
    first_image = images[0]
    
    print(f"Saving GIF as {output_filename}...")
    first_image.save(
        output_filename,
        save_all=True,
        append_images=images[1:],
        optimize=True,  # <-- Set to True for smaller file size
        duration=FRAME_DURATION_MS,
        loop=0
    )
    
    # Get final file size for display
    file_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"✨ Success! GIF created: {output_filename} ({file_size_mb:.2f} MB)")