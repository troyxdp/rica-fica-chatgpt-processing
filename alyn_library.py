from Alyn.alyn.skew_detect import SkewDetect
from Alyn.alyn.deskew import Deskew

# github link https://github.com/kakul/Alyn

print("\n")
img_path = 'skew-docs-1/27 Crete Utility bill-skewed.jpg'
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