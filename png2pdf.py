import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import PyPDF2


def merge_pngs_to_pdf(folder_path, output_file_name):
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
    output_file_path = os.path.join(folder_path, output_file_name)

    # Save images to a PDF
    rgb_images[0].save(output_file_path, save_all=True, append_images=rgb_images[1:])


def compress_pdf(input_pdf_path, output_pdf_path, quality=20):
    # Convert PDF to images
    images = convert_from_path(input_pdf_path)

    # Save the images back to a new compressed PDF with reduced resolution
    images[0].save(
        output_pdf_path,
        save_all=True,
        append_images=images[1:],
        resolution=quality,
        quality=95,
    )


def ocr_pdf(input_pdf_path, output_pdf_path):
    # Convert PDF to images
    images = convert_from_path(input_pdf_path)

    # Use pytesseract to OCR each image
    ocr_texts = []
    for img in images:
        ocr_texts.append(pytesseract.image_to_pdf_or_hocr(img, extension="pdf"))

    # Merge all OCRed PDFs into a single PDF
    with open(output_pdf_path, "wb") as out:
        pdf_merger = PyPDF2.PdfMerger()
        for text in ocr_texts:
            pdf_merger.append(PyPDF2.PdfFileReader(text))
        pdf_merger.write(out)


if __name__ == "__main__":
    directory = input("Enter the directory path containing the PNG files: ").strip()
    output_filename = input(
        "Enter the name of the output PDF file (e.g., output.pdf): "
    ).strip()

    merge_pngs_to_pdf(directory, output_filename)
    print(f"PDF created as {os.path.join(directory, output_filename)}")

    compressed_output_filename = "compressed_" + output_filename
    compress_pdf(
        os.path.join(directory, output_filename),
        os.path.join(directory, compressed_output_filename),
    )
    print(
        f"Compressed PDF created as {os.path.join(directory, compressed_output_filename)}"
    )

    ocr_output_filename = "ocr_" + compressed_output_filename
    ocr_pdf(
        os.path.join(directory, compressed_output_filename),
        os.path.join(directory, ocr_output_filename),
    )
    print(f"OCRed PDF created as {os.path.join(directory, ocr_output_filename)}")
