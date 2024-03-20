from wand.image import Image
from pdf2image import convert_from_path
import PIL
import os

test_single_image = False
thresh_coeff = 0.1

if test_single_image:

    file_path = "skew-docs-1/2023-06 Vodacom-skewed.jpg"
    deskew_twice = True

    # Open image. Convert from pdf if necessary
    print("Testing...")
    if file_path[-4:] in ('.pdf', '.PDF'): # STILL NEED TO TEST
        img = convert_from_path(file_path)[0]
        img.save(f"{file_path[:-4]}.jpg", "JPEG")
        file_path = f"{file_path[:-4]}.jpg"

    # Deskew image
    with Image(filename=file_path) as image:
        image.deskew(thresh_coeff*image.quantum_range)
        if deskew_twice:
            image.deskew(thresh_coeff*image.quantum_range)
            image.save(filename=f"{file_path[:-4]}-deskewed-twice.png")
        else:
            image.save(filename=f"{file_path[:-4]}-deskewed.png")

else:

    input_dir = "/media/refraime/DATA2/Troy/chatgpt-rica-fica-api/rica-fica-chatgpt-processing/skew-docs-3"
    deskew_once = False
    deskew_twice = True

    files = os.listdir(input_dir)
    _files = files.copy()

    if deskew_once:
        # Deskew once
        print("Testing single deskew...")
        for file in _files:
            if file[-4:] in  ('.jpg', '.png') or file[-5:] == '.jpeg':
                with Image(filename=os.path.join(input_dir, file)) as image:
                    image.deskew(thresh_coeff*image.quantum_range)
                    image.save(filename=os.path.join(input_dir, f"{file[:-4]}-deskewed.png"))

    if deskew_twice:
        # Deskew twice
        print("Testing double deskew...")
        for file in _files:
            if file[-4:] in  ('.jpg', '.png') or file[-5:] == '.jpeg':
                with Image(filename=os.path.join(input_dir, file)) as image:
                    image.deskew(thresh_coeff*image.quantum_range)
                    image.deskew(thresh_coeff*image.quantum_range)
                    image.save(filename=os.path.join(input_dir, f"{file[:-4]}-deskewed-twice.png"))

print("Done testing")