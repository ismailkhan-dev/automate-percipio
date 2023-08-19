import os
from PIL import Image


def merge_pngs_to_pdf(folder_path):
    # List all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Filter only .png files
    png_files = [f for f in files if f.endswith(".png")]

    # Sort the files to ensure they are in the desired order
    png_files.sort()

    # Convert .png files to images
    images = [Image.open(os.path.join(folder_path, f)) for f in png_files]

    # Convert images to RGB (necessary for saving as PDF)
    rgb_images = [img.convert("RGB") for img in images]

    # Full path for output PDF
    output_file_path = os.path.join(folder_path, "output.pdf")

    # Save images to a PDF
    rgb_images[0].save(output_file_path, save_all=True, append_images=rgb_images[1:])


if __name__ == "__main__":
    directory = input("Enter the directory path containing the PNG files: ").strip()
    merge_pngs_to_pdf(directory)
    print(f"PDF created as {os.path.join(directory, 'output.pdf')}")
