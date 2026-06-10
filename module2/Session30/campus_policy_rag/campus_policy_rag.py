"""
Campus Policy RAG Assistant
Reads multiple PDF policy documents and answers student questions
using only the retrieved policy context.
"""

import os
import re
from pathlib import Path

from pypdf import PdfReader
import chromadb
from chromadb.config import Settings
from openai import OpenAI

# --- config ---
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "campus_policies"
CHUNK_SIZE_WORDS = 150
OVERLAP_WORDS = 20  # about 13% overlap
PDF_FOLDER = "./policy_documents"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"


def infer_policy_type(filename: str) -> str:
    """Figures out the policy type from the PDF filename."""
    fname_lower = Path(filename).stem.lower()
    if "hostel" in fname_lower:
        return "hostel"
    if "refund" in fname_lower:
        return "refund"
    if "library" in fname_lower:
        return "library"
    return "general"


def load_pdfs(folder: str):
    """Loads all PDFs from the given folder. Returns a list of dicts
    with text, source, and page info."""
    documents = []
    pdf_files = sorted(Path(folder).glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {folder}")
    for pdf_path in pdf_files:
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        for i, page in enumerate(reader.pages):
            raw_text = page.extract_text() or ""
            cleaned = clean_text(raw_text)
            if cleaned:
                documents.append({
                    "text": cleaned,
                    "source": pdf_path.name,
                    "page": i + 1,
                    "policy_type": infer_policy_type(pdf_path.name),
                })
        print(f"Loaded {num_pages} page(s) from: {pdf_path.name}")
    return documents


def clean_text(text: str) -> str:
    """Removes extra newlines and repeated spaces from extracted text."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE_WORDS, overlap: int = OVERLAP_WORDS):
    """Splits text into overlapping chunks of roughly chunk_size words."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def get_embedding_client():
    """Sets up the OpenAI client from env var."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def generate_embeddings(texts: list):
    """Generates embeddings for a list of texts using OpenAI."""
    client = get_embedding_client()
    response = client.embeddings.create(input=texts, model=EMBEDDING_MODEL)
    return [item.embedding for item in response.data]


def get_chroma_collection():
    """Returns a persistent ChromaDB collection."""
    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_or_create_collection(name=COLLECTION_NAME)


def build_knowledge_base(documents: list):
    """Chunks all docs, generates embeddings, and stores in ChromaDB."""
    collection = get_chroma_collection()
    all_chunks = []
    all_metadatas = []
    all_ids = []

    for doc in documents:
        chunks = split_into_chunks(doc["text"])
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}_p{doc['page']}_c{idx}"
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": doc["source"],
                "page": str(doc["page"]),
                "policy_type": doc["policy_type"],
            })
            all_ids.append(chunk_id)

    if not all_chunks:
        print("No chunks to store.")
        return

    print(f"Total chunks created: {len(all_chunks)}")
    embeddings = generate_embeddings(all_chunks)
    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas,
    )
    print(f"Successfully stored {len(all_chunks)} chunks in vector database.")


def retrieve_chunks(query: str, top_k: int = 3):
    """Converts query to embedding and retrieves top-k relevant chunks."""
    collection = get_chroma_collection()
    query_embedding = generate_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    return list(zip(chunks, metadatas))


def build_prompt(context: str, question: str) -> str:
    """Builds a prompt that tells the LLM to only use the provided context."""
    return (
        "You are a helpful campus policy assistant.\n\n"
        "Use ONLY the following policy context to answer the student's question.\n"
        "Do NOT use any outside knowledge.\n"
        "If the context does not contain the answer, say exactly:"
        ' "I don\'t have that information."\n'
        "Keep the answer simple and student-friendly.\n\n"
        f"--- Policy Context ---\n{context}\n\n"
        f"Student Question: {question}\n\n"
        "Answer:"
    )


def answer_question(question: str) -> str:
    """End-to-end retrieval and generation for a single question."""
    retrieved = retrieve_chunks(question, top_k=3)
    print(f"Retrieved {len(retrieved)} relevant chunk(s).")

    # combine retrieved chunks into a single context string
    context_parts = []
    for chunk, meta in retrieved:
        source = meta.get("source", "unknown")
        page = meta.get("page", "?")
        context_parts.append(f"[{source} - page {page}]\n{chunk}")
    context = "\n\n".join(context_parts)

    prompt = build_prompt(context, question)
    client = get_embedding_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful campus policy assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Campus Policy RAG Assistant")
    print("=" * 40)

    # build knowledge base
    print("\n--- Building Knowledge Base ---")
    docs = load_pdfs(PDF_FOLDER)
    build_knowledge_base(docs)
    print(f"\nVector DB ready. Collection: {COLLECTION_NAME}")

    # test queries
    test_queries = [
        "Can I get a refund after dropping a course?",
        "What is the deadline for returning a library book?",
        "Are hostel visitors allowed on weekends?",
    ]

    print("\n--- Answering Student Queries ---\n")
    for query in test_queries:
        print(f"User Query: {query}")
        answer = answer_question(query)
        print(f"Answer: {answer}\n")
