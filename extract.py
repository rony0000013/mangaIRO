from zipfile import ZipFile
import os
import shutil
from PIL import Image
import sys
import random
import glob
from tqdm import tqdm


def convert_to_black_and_white(color_folder, output_directory):
    """
    Converts the input image to black and white and saves it in the specified output directory.

    Args:
      input_image: Path to the input image file.
      output_directory: Path to the directory where the black and white image will be saved.
    """
    os.makedirs(output_directory, exist_ok=True)
    for root, dirs, files in os.walk(color_folder):
        for file in tqdm(files, desc=f"Converting images to B&W of {os.path.basename(cbz_filename)}"):
            input_image = os.path.join(root, file)
            # Open the input image
            image = Image.open(input_image)

            # Convert the image to black and white
            bw_image = image.convert("L")

            # Save the black and white image in the output directory
            output_image = os.path.join(output_directory, os.path.basename(input_image))
            bw_image.save(output_image)



def extract_cbz_images(cbz_filename, output_folder, i):
    """
    Extracts JPG images from a CBZ file to the specified output folder.

    Args:
      cbz_filename: Path to the CBZ file.
      output_folder: Path to the folder where extracted images will be saved.
      i: Index of the CBZ file in the directory.
    """
    with ZipFile(cbz_filename, "r") as zip_ref:
        zip_ref.extractall(output_folder)

    # Create color and bw folders in the output folder
    color_folder = os.path.join(output_folder, "color")
    os.makedirs(color_folder, exist_ok=True)

    # Move the extracted images to the color folder
    for root, dirs, files in os.walk(output_folder):
        if "color" in dirs:
            dirs.remove("color")
        if "bw" in dirs:
            dirs.remove("bw")
        for file in files:
            if file.endswith(".cbz"):
                continue
            src_path = os.path.join(root, file)
            dst_path = os.path.join(color_folder, f"{file.split('.')[0]}_{i}.{file.split('.')[-1]}")
            shutil.move(src_path, dst_path)

    # Delete all folders in output folder except for the folders "color" and "bw"
    for root, dirs, files in os.walk(output_folder):
        for dir in dirs:
            if dir not in ["color", "bw"]:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)


def split_files(color_folder, bw_folder, train_folder, val_folder, split):
    """
    Split the files in the color and bw folders into train and val folders based on the split value,
    ensuring that the split is identical for files with the same names in both folders.

    Args:
        color_folder: Path to the color folder.
        bw_folder: Path to the bw folder.
        train_folder: Path to the train folder.
        val_folder: Path to the val folder.
        split: Split value between 0 and 1 indicating the proportion of files to be used for training.
    """

    # Get the list of filenames in the color folder
    color_files = [os.path.basename(file) for file in glob.glob(os.path.join(color_folder, "*"))]

    # Shuffle the list of filenames
    random.shuffle(color_files)

    # Calculate the split index
    split_index = int(len(color_files) * split)

    # Split the filenames into train and val sets
    train_filenames = color_files[:split_index]
    val_filenames = color_files[split_index:]

    # Function to move files from source to destination folder
    def move_files(filenames, src_folder, dst_folder):
        for filename in filenames:
            src_path = os.path.join(src_folder, filename)
            dst_path = os.path.join(dst_folder, filename)
            shutil.move(src_path, dst_path)

    # Create subfolders for color and bw in train and val folders
    train_color_folder = os.path.join(train_folder, 'color')
    val_color_folder = os.path.join(val_folder, 'color')
    os.makedirs(train_color_folder, exist_ok=True)
    os.makedirs(val_color_folder, exist_ok=True)

    # Move the color and bw files to their respective train and val folders
    move_files(train_filenames, color_folder, train_color_folder)
    move_files(val_filenames, color_folder, val_color_folder)

    if bw_folder:
        train_bw_folder = os.path.join(train_folder, 'bw')
        val_bw_folder = os.path.join(val_folder, 'bw')
    
        os.makedirs(train_bw_folder, exist_ok=True)
        os.makedirs(val_bw_folder, exist_ok=True)
    
        move_files(train_filenames, bw_folder, train_bw_folder)
        move_files(val_filenames, bw_folder, val_bw_folder)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract.py <directory> <split>")
        sys.exit(1)

    directory = sys.argv[1]
    split = float(sys.argv[2])
    output_folder = "data"

    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for i, file in enumerate(tqdm(files, desc="Extracting images")):
                if file.endswith(".cbz"):
                    cbz_filename = os.path.join(root, file)
                    extract_cbz_images(cbz_filename, output_folder, i+62)
        # convert_to_black_and_white(os.path.join(output_folder, "color"), os.path.join(output_folder, "bw"))
    else:
        extract_cbz_images(directory, output_folder, 1)

    # split_files(color_folder=os.path.join(output_folder, "color"), bw_folder= None, train_folder=os.path.join(output_folder, "train"), test_folder=os.path.join(output_folder, "test"), split=split)
    # split_files(os.path.join(output_folder, "color"), os.path.join(output_folder, "bw"), os.path.join(output_folder, "train"), os.path.join(output_folder, "val"), split)

    # shutil.rmtree(os.path.join(output_folder, "color"))
    # shutil.rmtree(os.path.join(output_folder, "bw"))