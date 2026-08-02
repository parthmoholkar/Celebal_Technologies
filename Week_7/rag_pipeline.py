import warnings
warnings.filterwarnings("ignore")

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from transformers import pipeline

try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

QA_PROMPT = PromptTemplate.from_template(
    "Answer the question using only the context below. "
    "If the answer is not in the context, say you don't know.\n\n"
    "Context:\n{context}\n\n"
    "Question: {input}\n\n"
    "Answer:"
)


def load_and_chunk(pdf_path, chunk_size=300, chunk_overlap=50):
    reader = PdfReader(pdf_path)
    pages = [
        Document(page_content=page.extract_text(), metadata={"page": i})
        for i, page in enumerate(reader.pages)
    ]
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(pages)


def build_vector_store(chunks):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embedding_model)


def load_llm():
    
    generation_pipeline = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_new_tokens=200
    )
    return HuggingFacePipeline(pipeline=generation_pipeline)


def build_qa_chain(pdf_path):
    chunks = load_and_chunk(pdf_path)
    vector_store = build_vector_store(chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = load_llm()
    document_chain = create_stuff_documents_chain(llm, QA_PROMPT)
    return create_retrieval_chain(retriever, document_chain)