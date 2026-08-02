# Document Question Answering System (RAG)

A Streamlit app that answers questions grounded in the content of an uploaded PDF, using a retrieval-augmented generation pipeline. Every component runs locally - no API key or paid account needed.

## How it works

1. The uploaded PDF is split into overlapping text chunks.
2. Each chunk is embedded with `sentence-transformers/all-MiniLM-L6-v2` and stored in a FAISS index.
3. A question is embedded the same way and used to retrieve the most relevant chunks.
4. `google/flan-t5-base` generates an answer using only those retrieved chunks as context.

## Setup

```bash
git clone <this-repo-url>
cd week7_Parth_Moholkar
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

This opens the app in your browser. Upload a PDF, wait for it to process (downloads two small models the first time), then ask a question.

## Files

- `app.py` - Streamlit interface: file upload, question input, answer display
- `rag_pipeline.py` - document loading, chunking, embeddings, vector store, and the RAG chain
- `requirements.txt` - project dependencies
