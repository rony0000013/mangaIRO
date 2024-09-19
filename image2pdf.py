from PIL import Image
import os, sys, re
from tqdm import tqdm


def extract_number(filename):
    match = re.search(r'pdf_(\d+)_', filename)
    return int(match.group(1)) if match else float('inf')


def convert_images_to_pdf(folder_path, output_path):
    images = []
    for filename in tqdm(sorted(os.listdir(folder_path), key=extract_number)):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            width, height = image.size
            scaled_image = image.resize((int(width * .75), int(height * 1)), Image.LANCZOS)
            images.append(scaled_image)
            # images.append(image)

    if images:
        images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python image2pdf.py <folder_path> <output_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    output_path = sys.argv[2]
    convert_images_to_pdf(folder_path, output_path)