# A script to increase the exposure of all JPG images in a folder.
# It processes files in alphabetical order.
# It prompts the user for an exposure factor, then creates new, brighter images.
# The original images are not modified.
#
# Required library: Pillow
# Install it using: pip install Pillow

from PIL import Image, ImageEnhance
import glob
import os

def increase_exposure_sorted():
    """
    Finds all .jpg files in the current directory, sorts them alphabetically,
    asks for an exposure factor, and saves new, brighter versions.
    """
    # --- 1. Get User Input for Exposure Factor ---
    exposure_factor = 0.0
    while True:
        try:
            # Prompt the user for the desired increase
            value = input("Enter the exposure increase factor (e.g., 1.5 for 50% brighter): ")
            exposure_factor = float(value)
            if exposure_factor <= 1.0:
                print("⚠️ Please enter a factor greater than 1.0 to increase brightness.")
            else:
                break  # Exit the loop if input is valid
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    # --- 2. Find all JPG files in the directory ---
    print("\nSearching for images...")
    image_paths = glob.glob('*.jpg') + glob.glob('*.JPG')

    # --- NEW: Sort the list of files alphabetically ---
    image_paths.sort()

    if not image_paths:
        print("No JPG files found in this folder. Exiting.")
        return

    print(f"Found {len(image_paths)} JPG files. Processing in alphabetical order.")

    # --- 3. Process each image ---
    # Counter for the new filenames
    image_count = 1
    for image_path in image_paths:
        try:
            # Open the image file
            with Image.open(image_path) as img:
                # Use ImageEnhance.Brightness to adjust exposure
                enhancer = ImageEnhance.Brightness(img)
                img_enhanced = enhancer.enhance(exposure_factor)

                # Define the new filename: n-[exposure_amount].jpg
                new_filename = f"{image_count}-{exposure_factor}.jpg"

                # Save the new, brighter image
                img_enhanced.save(new_filename)
                print(f"✅ Processed '{image_path}' -> Saved as '{new_filename}'")

                image_count += 1

        except Exception as e:
            print(f"❌ Could not process '{image_path}'. Error: {e}")

    print("\n✨ All images processed successfully!")

if __name__ == '__main__':
    increase_exposure_sorted()