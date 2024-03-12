# from openai import OpenAI
import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  
img_path = "test-documents/test-utility-bill.jpg"
base64_img = encode_image(img_path)

headers = {
    "Content-Type" : "application/json",
    "Authorization" : f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give me a detailed description of the document in the image. Tell me what type of organisation issued it and what date it was issued, as well as if you can extract  any names and address details you could extract."
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
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())