from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_model = OpenAIEmbeddings()

def process_text_rag(query: str) -> str:
    """
    Performs text-based RAG using FAISS and returns GPT-4 response.
    """
    vectorstore = FAISS.load_local(
    "faiss_text_index",
    embedding_model,
    allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"Using the context below, answer the medical query:\n\n{context}\n\nQuestion: {query}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
