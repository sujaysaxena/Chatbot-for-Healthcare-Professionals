import numpy as np
import faiss
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from langchain_community.vectorstores import FAISS as TextFAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import os

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
openai_embed = OpenAIEmbeddings()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEXT_INDEX_PATH = "faiss_text_index"
IMAGE_INDEX_PATH = "faiss_image_index"
IMAGE_META_PATH = "faiss_image_metadata.npy"

# 🔍 TEXT QUERY
def query_text_rag(text_query: str):
    vectorstore = TextFAISS.load_local(TEXT_INDEX_PATH, openai_embed)
    docs = vectorstore.similarity_search(text_query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"Use the following medical context to answer:\n\n{context}\n\nQ: {text_query}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# 🖼️ IMAGE QUERY
def query_image_rag(image: Image.Image, user_question: str):
    inputs = clip_processor(images=image, return_tensors="pt")
    image_emb = clip_model.get_image_features(**inputs).detach().numpy().astype("float32")

    index = faiss.read_index(IMAGE_INDEX_PATH)
    metadata = np.load(IMAGE_META_PATH, allow_pickle=True)

    _, indices = index.search(image_emb, k=3)
    matched = [metadata[i] for i in indices[0]]

    # Generate GPT prompt from image context
    prompt = (
        f"The user uploaded a medical image and asked: '{user_question}'.\n"
        f"Here are related images from memory:\n" +
        "\n".join([f"- Similar image: {os.path.basename(m['image_path'])}" for m in matched]) +
        "\n\nGenerate a helpful and medically sound response."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
