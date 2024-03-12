# from openai import OpenAI
import base64
import requests
import json

# OPENAI API KEY
api_key = "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"

# FUNCTION TO ENCODE THE IMAGE
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
img_path = "test-documents/test-utility-bill.jpg" # 691px x 1536px
base64_img = encode_image(img_path)

# HEADERS USED BY REQUESTS
headers = {
    "Content-Type" : "application/json",
    "Authorization" : f"Bearer {api_key}"
}

# EXTRACT INFO FROM THE DOCUMENT
# Create prompt to be sent with image giving extraction instructions
extract_text_prompt = """
    Give me a detailed description of the document in the image. Tell me what is the... 
    - Issuing authority
    - Issued date
    - Addressee name
    - Address
    from the document.

    Also, give me a rough check on the authenticity of the document. Check the...
    - Consistency in fonts
    - Consistency in alignments
    - Quality of logos
    - Quality of text
    - Legibility
    - Professionalism
    of the document. 

    Return your result in json format, and make each of the above criteria a field in the json
    object. For the rough check of authenticity, return the result of each field as a true/false 
    value. If you cannot extract a certain field listed above, put 'unknown'. 

    Include nothing else in the output besides the json output.
"""
# Create json payload that will be sent in the post request
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
                        "url": f"data:image/jpeg;base64,{base64_img}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 2000
}
# Send request
extract_text_response = requests.post(
        "https://api.openai.com/v1/chat/completions", 
        headers=headers, 
        json=extract_info_payload
    )
# Extract json response and print it
extract_response_str = extract_text_response.json()["choices"][0]["message"]["content"][8:-4]
print(extract_response_str)

extract_json = json.loads(extract_response_str)
print("")
print(extract_json)