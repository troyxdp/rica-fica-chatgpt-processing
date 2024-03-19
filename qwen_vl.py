from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch


# NEED TO RUN COMMAND export HF_HOME=/media/refraime/DATA2/Troy/huggingface


image = "test-documents-proof-of-residence/test-utility-bill-cropped.jpg"

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="cpu", trust_remote_code=True).eval()
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)

prompt = """
    Give me a detailed description of the document in the image. Tell me what is the... 
    - Document type
    - Document name
    - Issuing authority
    - Issued date (DD/MM/YYYY format)
    - Addressee full name
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

    Also, give me a check on the quality of the document. Tell me about the...
    - Resolution (state whether it is high/medium/low)
    - If it is in colour (state as true/false)
    - How blurry it is (state as high/medium/low)

    Also, check that the issuing date is within three months of the current date, i.e. if the issuing
    date is within 3 months of the current date. Call this field 'isCurrent'.

    Remember to take the orientation of the document into account. 

    Return your result in json format, and make each of the above criteria a field in the json
    object. For the rough check of authenticity, return the result of each field as a true/false 
    value, and make sure isCurrent is also a true/false value. For the quality check, give me the data
    I specified. If you cannot extract a certain field listed above, put 'unknown'. 

    Include nothing else in the output besides the json output. Make the field names snake case,
    but keep the values of the field in normal case. Make sure the values of the fields are not in 
    snake case. 
"""

query = tokenizer.from_list_format([
    {'image': image}, # Either a local path or an url
    {'text': prompt},
])

inputs = tokenizer(query, return_tensors='pt')
inputs = inputs.to(model.device)
pred = model.generate(**inputs)
response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=False)
print(response)