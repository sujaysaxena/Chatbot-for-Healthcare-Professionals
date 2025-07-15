from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration
from openai import OpenAI
import torch
import io
import os

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Main function used in main.py
async def analyze_medical_image(file):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    extracted_text = pytesseract.image_to_string(image)

    if extracted_text.strip():
        gpt_input = f"Analyze this medical text:\n{extracted_text}"
        method = "OCR"
    else:
        inputs = processor(image, return_tensors="pt").to(device)
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)
        gpt_input = f"Analyze this medical image caption:\n{caption}"
        method = "BLIP"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": gpt_input}],
        temperature=0.3,
        max_tokens=500
    )

    return {
        "method": method,
        "summary_input": extracted_text.strip() if method == "OCR" else caption,
        "response": response.choices[0].message.content.strip()
    }
