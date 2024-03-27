import os
import glob
import shutil
import argparse


parser = argparse.ArgumentParser("Move images to rgb folder")
parser.add_argument('--path', type=str, required=True)
configs = parser.parse_args()

out_dir = os.path.join(configs.path, 'sorted')

os.makedirs(out_dir, exist_ok=True)

img_files = sorted(glob.glob(os.path.join(configs.path, "*.jpg")))

for i, img_file in enumerate(img_files):
    src = img_file
    file_name = str(i).zfill(6) + '.jpg'

    dst = os.path.join(out_dir, file_name)
    shutil.move(src, dst)    
