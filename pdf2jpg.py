import os
from pdf2image import convert_from_path

input_dir = "skew-docs-4"

for file in os.listdir(input_dir):
    if file[-4:] in ('.pdf', '.PDF'):
        img = convert_from_path(os.path.join(input_dir, file))[0]
        img.save(os.path.join(input_dir, f"{file[:-4]}.jpg"), "JPEG")