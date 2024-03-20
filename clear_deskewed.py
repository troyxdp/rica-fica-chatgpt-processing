import os

input_dir = "/media/refraime/DATA2/Troy/chatgpt-rica-fica-api/rica-fica-chatgpt-processing/skew-docs-2"
files_ = os.listdir(input_dir)
files = files_.copy()

for file in files:
    if file.__contains__("deskewed"):
        os.remove(os.path.join(input_dir, file))