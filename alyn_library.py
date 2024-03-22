from Alyn.alyn.skew_detect import SkewDetect
from Alyn.alyn.deskew import Deskew
import os

# github link https://github.com/kakul/Alyn

print("\n")
test_single_image = False

if test_single_image:

    img_path = 'scanned-or-photographed/2Doc1-skewed.jpg'

    img_name = img_path.split("/")[-1]
    sd = SkewDetect(
            input_file=img_path,
            display_output="yes"
        )
    sd.run()
    d = Deskew(
            input_file=img_path,
            display_image=True,
            output_file = f'/media/refraime/DATA2/Troy/chatgpt-rica-fica-api/rica-fica-chatgpt-processing/deskewed_images/{img_name}',
            r_angle=0
        )
    d.run()

else:

    input_dir = "/media/refraime/DATA2/Troy/chatgpt-rica-fica-api/rica-fica-chatgpt-processing/skew-docs-4"

    files_ = os.listdir(input_dir)
    files = files_.copy()

    for file in files:
        img_path = os.path.join(input_dir, file)
        img_name = img_path.split("/")[-1]

        if file.__contains__("skewed"):
            sd = SkewDetect(
                input_file=img_path,
                display_output="yes"
            )
            sd.run()
            d = Deskew(
                    input_file=img_path,
                    display_image=False,
                    output_file = f'/media/refraime/DATA2/Troy/chatgpt-rica-fica-api/rica-fica-chatgpt-processing/deskewed_images/{img_name}',
                    r_angle=0
                )
            d.run()