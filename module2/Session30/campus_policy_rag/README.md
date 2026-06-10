# Campus Policy RAG Assignment

So this assignment was about building a RAG pipeline that can answer student questions based on institute policy PDFs. The idea is pretty simple — you load PDFs, chunk them, store in a vector DB, and then retrieve relevant chunks when someone asks a question.

## What I Built

A Python script `campus_policy_rag.py` that:
- Reads PDF policy documents from the `policy_documents/` folder
- Extracts and cleans text, then splits into overlapping chunks
- Stores chunks with embeddings in ChromaDB along with metadata
- Answers student queries by retrieving top 3 relevant chunks and using an LLM

I created 3 sample PDFs (hostel, refund, library policies) since real ones weren't available. Each has 2-3 paragraphs so the pipeline has something to retrieve from.

## How to Run

First, set your OpenAI API key (or you can use any other provider — just adapt the code):

```bash
export OPENAI_API_KEY="your-key-here"
pip install -r requirements.txt
python campus_policy_rag.py
```

## How It Works

1. `load_pdfs()` — walks through the policy_documents folder, reads each PDF page
2. `clean_text()` — removes extra spaces and newlines
3. `split_into_chunks()` — breaks text into 150-word chunks with 20-word overlap
4. `build_knowledge_base()` — embeds chunks and stores in ChromaDB with metadata
5. `answer_question()` — retrieves top 3 chunks, builds a strict prompt, and calls the LLM

The prompt explicitly tells the model to answer only from retrieved context and say "I don't have that information" when the answer isn't found.
