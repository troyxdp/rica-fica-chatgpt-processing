import os
import base64
import requests
import json
from skimage import io
from io import BytesIO
import numpy as np
import cv2
from Alyn.alyn.skew_detect import SkewDetect
from Alyn.alyn.deskew import Deskew



# OPENAI API KEY
API_KEY = "GET_FROM_TXT_FILE"
# FILE PATH TO IMAGE BEING PROCESSED
file_path = "skew-docs-4/vodacom-bill-skewed.jpg"
# BLURRINESS THRESHOLD
BLURRINESS_THRESHOLD = 1500



# FUNCTION TO DESKEW IMAGE
def deskew_image(image_path):
    # Deskew image
    deskew = Deskew(
            input_file=image_path,
            display_image=True
        )
    deskew.run()

    # Save deskewed image into memory
    deskewed_image = deskew.deskewed_image.astype(np.uint8)[:,:,:3]
    image_bytes = BytesIO()
    io.imsave(image_bytes, deskewed_image, format='JPEG')

    # Get the bytes data
    image_bytes.seek(0)
    image_data = image_bytes.getvalue()

    # Encode image and return it
    # return base64.b64encode(image_data)
    return image_data

# GET DESKEWED IMAGE
deskewed_img = deskew_image(file_path)



# DETECT BLURRINESS OF IMAGE
def is_blurry(image_path, blur_threshold):
    # DETECT THE BLURRINESS OF AN IMAGE USING THE LAPLACIAN
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < blur_threshold, laplacian_var
is_blurry, lap_var = is_blurry(file_path, 1700)

if is_blurry:
    print(f"Image is blurry. Laplacian Variance = {lap_var}")
    print("Pushing to manual queue...")
else:
    # CREATE PROMPT TO BE SENT WITH IMAGE GIVING EXTRACTION INSTRUCTIONS
    extract_text_prompt = """
        Give me a detailed description of the document in the image. Tell me what is the... 
        - Document type
        - Document name
        - Issuing authority
        - Issued date (DD/MM/YYYY format)
        - Addressee full name (in all caps)
        - Address (in format STREET, AREA, POSTAL CODE)
        from the document.

        Also, give me a rough check on the authenticity of the document. Check the...
        - Consistency in fonts
        - Consistency in alignments
        - Quality of logos
        - Quality of text
        - Legibility
        - Professionalism
        of the document. 

        Also, give me a check on the quality of the document. Tell me about the...
        - Resolution (state whether it is high/medium/low)
        - If it is in colour (state as true/false)
        - How blurry it is (state as high/medium/low)

        Also, check that the issuing date is within three months of the current date, i.e. if the issuing
        date is within 3 months of the current date. Call this field 'is_current'. If the issuing date of
        the document is within 3 months of the current date, set is_current to True, otherwise set is
        to False. 

        Remember to take the orientation of the document into account. 

        Return your result in json format, and make each of the above criteria a field in the json
        object. For the rough check of authenticity, return the result of each field as a true/false 
        value, and make sure isCurrent is also a true/false value. For the quality check, give me the data
        I specified. If you cannot extract a certain field listed above, put 'unknown'. 

        Include nothing else in the output besides the json output. Make the field names snake case,
        but keep the values of the field in normal case. Make sure the values of the fields are not in 
        snake case. 
    """



    # PREP DATA FOR CHATGPT
    try:
        # CREATE TEMPORARY JPG FILE AND BASE64 ENCODE IT
        # Create json payload that will be sent in the post request
        with open('temp_files/temp_img.jpg', 'wb') as jpg:
            jpg.write(deskewed_img)
        # Create payload to send to ChatGPT
        with open('temp_files/temp_img.jpg', 'rb') as jpg:
            # Encode image
            b64_encoded_img = base64.b64encode(jpg.read()).decode('utf-8')

        # HEADERS USED BY POST REQUEST
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {API_KEY}"
        }
        # PAYLOAD
        extract_info_payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": extract_text_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                            {
                                "url": f"data:image/jpeg;base64,{b64_encoded_img}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000
        }

    except Exception as e:
        print("Error: could not prep payload for ChatGPT")
        print(e)



    # SEND REQUEST AND EXTRACT RESPONSE
    json_str=""
    try:
        # SEND REQUEST AND DELETE TEMP FILE
        extract_text_response = requests.post(
                "https://api.openai.com/v1/chat/completions", 
                headers=headers, 
                json=extract_info_payload
            )
        os.remove('temp_files/temp_img.jpg')

        # EXTRACT JSON RESPONSE AND PRINT IT
        response = extract_text_response.json()
        json_str = response["choices"][0]["message"]["content"][8:-4]
        print(json_str)
    except Exception as e:
        print("Error: could not send request or could not successfully extract data from response")
        print(e)



    # EXTRACT JSON FROM RESPONSE STRING
    extract_json = None
    try:
        extract_json = json.loads(json_str)
        print("")
        print(extract_json)
    except Exception as e:
        print("There was an error in extracting a JSON object from the response")
        print(e)

    if extract_json is None or extract_json["addressee_full_name"] == 'unknown' or extract_json['address'] == 'unknown':
        print("Pushing to manual queue...")
        # Here you would send (original) document to manual queue
    else:
        print("Successfully extracted data")
        # Here you would check if the data is correct - something like...
        # 
        # if data.is_incorrect:
        #     send_to_manual_queue(file_path)
        # else:
        #     return "Data is valid"