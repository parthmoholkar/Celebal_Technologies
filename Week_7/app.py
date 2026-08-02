import streamlit as st
from rag_pipeline import build_qa_chain

st.set_page_config(page_title="Document Question Answering (RAG)")
st.title("Document Question Answering System")
st.caption("Upload a PDF and ask questions grounded in its actual content - no API key required.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    if st.session_state.get("uploaded_name") != uploaded_file.name:
        with open("uploaded_document.pdf", "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("Processing document - this downloads two small models on first run"):
            st.session_state.qa_chain = build_qa_chain("uploaded_document.pdf")
            st.session_state.uploaded_name = uploaded_file.name
        st.success("Document ready")

    question = st.text_input("Ask a question about the document")

    if st.button("Get Answer") and question:
        with st.spinner("Retrieving and generating answer..."):
            result = st.session_state.qa_chain.invoke({"input": question})

        st.subheader("Answer")
        st.write(result["answer"].strip())

        with st.expander("Retrieved context"):
            for i, doc in enumerate(result["context"], start=1):
                st.markdown(f"**Chunk {i}:** {doc.page_content}")
else:
    st.info("Upload a PDF to get started")
