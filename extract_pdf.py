import os, sys
from pdf2image import convert_from_path
from tqdm import tqdm

def extract_images_from_pdfs(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in tqdm(os.listdir(input_folder), desc="Extracting images from PDFs"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            # Convert PDF to a list of images
            # convert_from_path(pdf_path, poppler_path=r"C:\Users\rony0\Downloads\poppler-24.02.0\Library\bin", output_folder=output_folder, thread_count=12, fmt="png")

            images = convert_from_path(pdf_path, poppler_path=r"C:\Users\rony0\Downloads\poppler-24.02.0\Library\bin", thread_count=12, fmt="png")

            # # Iterate over all images and save them
            for page_num, image in enumerate(tqdm(images, desc=f"{filename}")):
                image_path = os.path.join(output_folder, f"{filename}_{page_num}.png")
                image.save(image_path, "PNG")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    extract_images_from_pdfs(input_folder, output_folder)