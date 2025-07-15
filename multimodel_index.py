import os
import numpy as np
import faiss
from transformers import CLIPModel, CLIPProcessor
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS as TextFAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from PIL import Image
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Init models
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
openai_embed = OpenAIEmbeddings()

TEXT_INDEX_PATH = "faiss_text_index"
IMAGE_INDEX_PATH = "faiss_image_index"
IMAGE_META_PATH = "faiss_image_metadata.npy"

# 🧠 TEXT VECTOR INDEX
def build_text_index(pdf_dir="data"):
    print("🔍 Building text index...")
    
    docs = []
    for fname in os.listdir(pdf_dir):
        if fname.endswith(".pdf"):
            print(f"📄 Loading PDF: {fname}")
            loader = PyPDFLoader(os.path.join(pdf_dir, fname))
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    print(f"✂️ Split into {len(chunks)} chunks")

    vectorstore = TextFAISS.from_documents(chunks, openai_embed)
    vectorstore.save_local(TEXT_INDEX_PATH)

    print(f"✅ Text index built and saved to: {TEXT_INDEX_PATH}")

# 🧠 IMAGE VECTOR INDEX
def build_image_index(img_dir="data/medical_images"):
    print("🖼️ Building image index...")
    
    embeddings = []
    metadata = []

    for i, fname in enumerate(os.listdir(img_dir)):
        if fname.endswith((".png", ".jpg", ".jpeg")):
            print(f"📸 Processing image [{i + 1}]: {fname}")
            img_path = os.path.join(img_dir, fname)
            image = Image.open(img_path).convert("RGB")
            inputs = clip_processor(images=image, return_tensors="pt")
            image_emb = clip_model.get_image_features(**inputs).detach().numpy()[0]

            embeddings.append(image_emb)
            metadata.append({"image_path": img_path})

    if embeddings:
        embeddings = np.array(embeddings).astype("float32")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        faiss.write_index(index, IMAGE_INDEX_PATH)
        np.save(IMAGE_META_PATH, metadata)

        print(f"✅ Image index built and saved to: {IMAGE_INDEX_PATH}")
    else:
        print(f"⚠️ No valid images found in {img_dir}")

# 🔁 Run from terminal
if __name__ == "__main__":
    build_text_index(pdf_dir="data")
    build_image_index(img_dir="data")
