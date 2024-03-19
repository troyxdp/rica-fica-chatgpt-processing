import cv2
import numpy as np
import pytesseract

# NOTES:
# - Can use 

def scale_image(image, scale=1):
    return cv2.resize(image, dsize=(0,0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

def resize_image(image, new_dimensions):
    return cv2.resize(image, dsize=new_dimensions, interpolation=cv2.INTER_CUBIC)

def convert_to_greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def adjust_contrast(image, alpha=1.0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

def apply_median_blur(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)

def apply_adaptive_threshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 5, 2)

def apply_threshold(image, thresh=191):
    return cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    # return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def correct_aspect_ratio(image, desired_width, desired_height):
    # This is a simple rescale. Specific corrections might require more complex logic.
    return cv2.resize(image, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

def dilate(image, kernel_size=(3,3), iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.dilate(image, kernel, iterations=iterations)
def erode(image, kernel_size=(3,3), iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.erode(image, kernel, iterations=iterations)
def open_morph(image, kernel_size=(1,1), iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    img = erode(image, kernel_size, iterations)
    return dilate(img, kernel_size, iterations)
def close_morph(image, kernel_size=(1,1), iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    img = dilate(image, kernel_size, iterations)
    return erode(img, kernel_size, iterations)

def segment_lines(image):
    # This is a simplified example. Real-world line segmentation may require more sophisticated logic.
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lines = [cv2.boundingRect(contour) for contour in contours]
    # Sort by Y position (top to bottom)
    lines.sort(key=lambda x: x[1])
    return lines



# IMAGE FILE TO PROCESS
IMAGE_NAME = "test-isolated-text/test-utility-bill-cropped-address-1.jpg"



# PREPROCESSING PARAMS
# Resize Params
SCALE = 1.0
OUTPUT_SIZE = (600, 480)
# Contrast Adjust Params
CONTRAST_ALPHA = 1.2
# Smoothing Params
SMOOTH_KERNEL_SIZE = 3
# Thresholding Params
THRESH = 200
# Dilation/Erosion Params
MORPH_KERNEL_SIZE = (2, 2)

# STEPS TO INCLUDE IN PREPROCESSING
# 1. resize
# 2. greyscale
# 3. adjust contrast
# 4. denoising
# 5. smooth
# 6. threshold (0 normal, 1 adaptive)
# 7. apply morphology (0 no, 1 dilate, 2 erode, 3 close, 4 open)
include_steps = [True, True, True, False, False, 0, 0]



# GET IMAGE
image = cv2.imread(IMAGE_NAME)
img = image.copy()
cv2.imshow('Original Image', img)
cv2.waitKey(0)

# 1. RESIZE IMAGE
if include_steps[0]:
    # img = scale_image(img, SCALE)
    img = resize_image(img, OUTPUT_SIZE)
    cv2.imshow('Resized Image', img)
    cv2.waitKey(0)

# 2. CONVERT TO GREYSCALE
if include_steps[1]:
    img = convert_to_greyscale(img)
    cv2.imshow('Greyscale', img)
    cv2.waitKey(0)

# 3. ENHANCE CONTRAST
if include_steps[2]:
    img = adjust_contrast(img, alpha=CONTRAST_ALPHA)
    cv2.imshow('Enhanced Contrast', img)
    cv2.waitKey(0)

# 4. DENOISE
if include_steps[3]:
    img = cv2.fastNlMeansDenoising(img, None, 10, 10, 7)
    cv2.imshow('Denoised Image', img)
    cv2.waitKey(0)

# 5. SMOOTH USING BLUR
if include_steps[4]:
    img = apply_median_blur(img, SMOOTH_KERNEL_SIZE)
    cv2.imshow('Smoothed Image', img)
    cv2.waitKey(0)

# 6. THRESHOLD IMAGE
if include_steps[5] == 0:
    img = apply_threshold(img, thresh=THRESH)
else:
    img = apply_adaptive_threshold(img)
cv2.imshow('Thresholded Image', img)
cv2.waitKey(0)

# Here you would do deskewing and aspect ratio correction according to ChatGPT

# 7. APPLY MORPHOLOGY
if not include_steps[6] == 0:
    if include_steps[6] == 1:
        img = dilate(img, MORPH_KERNEL_SIZE)
    elif include_steps[6] == 2:
        img = dilate(img, MORPH_KERNEL_SIZE)
    elif include_steps[6] == 3:
        img = close_morph(img, MORPH_KERNEL_SIZE)
    else:
        img = open_morph(img, MORPH_KERNEL_SIZE)
    cv2.imshow('Eroded Image', img)

# Extract Text
text = pytesseract.image_to_string(img)
print(text)
cv2.waitKey(0)

# TERMINATE PROGRAM
cv2.destroyAllWindows()

# TODO test deskewing and aspect ratio correction