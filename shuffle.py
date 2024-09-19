import os, sys
import random
import shutil

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python shuffle.py <input_folder> <output_folder> <split>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    split = float(sys.argv[3])
    os.makedirs(os.path.join(output_folder, "train"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "test"), exist_ok=True)

    file_list = os.listdir(input_folder)
    random.shuffle(file_list)

    split_index = int(len(file_list) * split)
    train_files = file_list[:split_index]
    test_files = file_list[split_index:]

    for file in train_files:
        shutil.move(os.path.join(input_folder, file), os.path.join(output_folder, "train", file))

    for file in test_files:
        shutil.move(os.path.join(input_folder, file), os.path.join(output_folder, "test", file))