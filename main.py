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

text =  "Give me a detailed description of the document in the image. "
text += "Tell me what type of organisation issued it and what date it was issued, "
text += "as well as any names and address details you could extract. "
text += "Return the results to me in json format. "
text += "Include issuing authority, issued date, addressee name, and address. "
text += "If you cannot extract a certain field listed above, put 'unknown'. "
text += "Include nothing else in the message besides the json output."

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
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

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

response_str = response.json()["choices"][0]["message"]["content"][8:-4]
print(response_str)