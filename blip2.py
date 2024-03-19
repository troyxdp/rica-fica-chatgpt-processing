from PIL import Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration
import torch
import os

os.environ["HF_HOME"] = "/media/refraime/DATA2/Troy/huggingface"

img_path = "test-documents-proof-of-residence/test-utility-bill-cropped.jpg"
image = Image.open(img_path).convert('RGB')  

processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

prompt = "This document is addressed to"
inputs = processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)
generated_ids = model.generate(**inputs, max_new_tokens=20)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(generated_text)