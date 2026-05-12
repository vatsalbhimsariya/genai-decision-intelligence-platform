import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="GenAI Decision Intelligence Platform",
    layout="wide"
)

# =====================================================
# LOAD ENV VARIABLES
# =====================================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =====================================================
# API KEY VALIDATION
# =====================================================
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# =====================================================
# VECTOR DATABASE PATH
# =====================================================
VECTOR_DIR = "vector_store"
VECTOR_INDEX_PATH = os.path.join(VECTOR_DIR, "faiss_index")

os.makedirs(VECTOR_DIR, exist_ok=True)

# =====================================================
# SESSION STATE
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

# =====================================================
# CACHED EMBEDDINGS
# =====================================================
@st.cache_resource
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# =====================================================
# CACHED LLM
# =====================================================
@st.cache_resource
def get_llm(api_key):

    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

# =====================================================
# LOAD VECTOR STORE
# =====================================================
@st.cache_resource
def load_vector_store(index_path):

    if not os.path.exists(index_path):
        return None

    embeddings = get_embeddings()

    try:

        vector_store = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return vector_store

    except Exception:
        return None

# =====================================================
# INITIALIZE COMPONENTS
# =====================================================
llm = get_llm(GROQ_API_KEY)

if st.session_state.vector_store is None:

    loaded_store = load_vector_store(VECTOR_INDEX_PATH)

    if loaded_store is not None:

        st.session_state.vector_store = loaded_store
        st.session_state.document_uploaded = True

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🧠 AI Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Upload PDF",
        "AI Chat",
        "About"
    ]
)

# =====================================================
# EXPERT MODE SELECTOR
# =====================================================
analysis_mode = st.sidebar.selectbox(
    "Analysis Mode",
    [
        "General Assistant",
        "Business Analyst",
        "Research Assistant",
        "Resume Reviewer",
        "Financial Advisor"
    ]
)

st.sidebar.markdown("---")

# =====================================================
# CLEAR CHAT
# =====================================================
if st.sidebar.button("🧹 Clear Chat"):

    st.session_state.messages = []
    st.rerun()

# =====================================================
# CLEAR DOCUMENTS
# =====================================================
if st.sidebar.button("🗑️ Clear Documents"):

    st.session_state.vector_store = None
    st.session_state.document_uploaded = False
    st.session_state.messages = []

    if os.path.exists(VECTOR_INDEX_PATH):

        shutil.rmtree(
            VECTOR_INDEX_PATH,
            ignore_errors=True
        )

    st.rerun()

# =====================================================
# HOME PAGE
# =====================================================
if page == "Home":

    st.title("🧠 GenAI Decision Intelligence Platform")

    st.markdown("""
    ## Features

    - Multi-PDF Upload
    - Conversational AI
    - Semantic Search
    - RAG Pipeline
    - Vector Database
    - Persistent Vector Storage
    - Explainable AI
    - Source Citations
    - Downloadable AI Reports
    - Expert AI Modes
    """)

    st.success("System Ready")

# =====================================================
# PDF UPLOAD PAGE
# =====================================================
elif page == "Upload PDF":

    st.title("📄 Upload PDF Documents")

    uploaded_files = st.file_uploader(
        "Upload one or multiple PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        all_text = ""

        with st.spinner("Processing PDFs..."):

            for uploaded_file in uploaded_files:

                try:

                    pdf_reader = PdfReader(uploaded_file)

                    for page_data in pdf_reader.pages:

                        extracted = page_data.extract_text()

                        if extracted:
                            all_text += extracted + "\n"

                except Exception:

                    st.error(f"Error reading {uploaded_file.name}")

        if len(all_text.strip()) == 0:

            st.warning("No readable text found")
            st.stop()

        # =====================================================
        # TEXT SPLITTING
        # =====================================================
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        chunks = splitter.split_text(all_text)

        docs = [
            Document(page_content=chunk)
            for chunk in chunks
        ]

        # =====================================================
        # EMBEDDINGS
        # =====================================================
        embeddings = get_embeddings()

        # =====================================================
        # VECTOR DATABASE
        # =====================================================
        vector_store = FAISS.from_documents(
            docs,
            embeddings
        )

        vector_store.save_local(VECTOR_INDEX_PATH)

        st.session_state.vector_store = vector_store
        st.session_state.document_uploaded = True

        st.success("✅ PDFs Processed Successfully")
        st.success(f"✅ Total Chunks Created: {len(chunks)}")
        st.success("✅ Vector Database Saved")

        with st.expander("📑 Extracted Text Preview"):

            st.write(all_text[:4000])

# =====================================================
# AI CHAT PAGE
# =====================================================
elif page == "AI Chat":

    st.title("💬 Conversational RAG Assistant")

    st.info(f"Current Mode: {analysis_mode}")

    if not st.session_state.document_uploaded:

        st.warning("Please upload PDFs first")

    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # =====================================================
    # CHAT INPUT
    # =====================================================
    query = st.chat_input(
        "Ask questions about uploaded documents"
    )

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):

            st.markdown(query)

        # =====================================================
        # ASSISTANT RESPONSE
        # =====================================================
        with st.chat_message("assistant"):

            with st.spinner("Analyzing..."):

                context = ""
                docs_with_scores = []

                # =====================================================
                # DOCUMENT RETRIEVAL
                # =====================================================
                if st.session_state.vector_store is not None:

                    docs_with_scores = st.session_state.vector_store.similarity_search_with_score(
                        query,
                        k=4
                    )

                    retrieved_docs = [
                        doc for doc, score in docs_with_scores
                    ]

                    context = "\n\n".join([
                        doc.page_content
                        for doc in retrieved_docs
                    ])

                # =====================================================
                # MEMORY CONTEXT
                # =====================================================
                memory_context = ""

                for msg in st.session_state.messages[-6:]:

                    memory_context += f"""
                    {msg['role']}:
                    {msg['content']}
                    """

                # =====================================================
                # MODE-SPECIFIC SYSTEM PROMPT
                # =====================================================
                system_prompt = ""

                if analysis_mode == "General Assistant":

                    system_prompt = """
                    You are a helpful AI assistant.

                    Answer naturally and accurately.
                    Use uploaded document context whenever relevant.
                    """

                elif analysis_mode == "Business Analyst":

                    system_prompt = """
                    You are a business analyst.

                    Focus on:
                    - business insights
                    - opportunities
                    - operational improvements
                    - recommendations
                    """

                elif analysis_mode == "Research Assistant":

                    system_prompt = """
                    You are a research assistant.

                    Focus on:
                    - summarization
                    - research insights
                    - key findings
                    - technical explanations
                    """

                elif analysis_mode == "Resume Reviewer":

                    system_prompt = """
                    You are an expert resume reviewer.

                    Focus on:
                    - ATS optimization
                    - skill analysis
                    - resume improvements
                    - interview readiness
                    """

                elif analysis_mode == "Financial Advisor":

                    system_prompt = """
                    You are a financial advisor.

                    Focus on:
                    - financial insights
                    - cost analysis
                    - revenue opportunities
                    - financial risks
                    """

                # =====================================================
                # FINAL PROMPT
                # =====================================================
                prompt = f"""
                {system_prompt}

                IMPORTANT RULES:
                - Answer ONLY what user asks
                - Avoid hallucinations
                - Use document context if available
                - If answer is not in document, say clearly
                - Keep response concise but insightful

                Conversation Memory:
                {memory_context}

                Retrieved Document Context:
                {context}

                User Question:
                {query}
                """

                # =====================================================
                # GENERATE RESPONSE
                # =====================================================
                try:

                    response = llm.invoke(prompt)

                    answer = response.content

                except Exception as e:

                    answer = f"Error generating response: {str(e)}"

                # =====================================================
                # SHOW RESPONSE
                # =====================================================
                st.markdown(answer)

                # =====================================================
                # DOWNLOAD REPORT
                # =====================================================
                report = f"""
                GenAI Decision Intelligence Platform Report

                Analysis Mode:
                {analysis_mode}

                User Question:
                {query}

                AI Response:
                {answer}

                Retrieved Context:
                {context}
                """

                st.download_button(
                    label="📥 Download AI Report",
                    data=report,
                    file_name="ai_analysis_report.txt",
                    mime="text/plain"
                )

                # =====================================================
                # SAVE CHAT HISTORY
                # =====================================================
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                # =====================================================
                # SHOW SOURCES
                # =====================================================
                if docs_with_scores:

                    with st.expander("📚 Retrieved Sources"):

                        for i, (doc, score) in enumerate(docs_with_scores):

                            st.markdown(f"### Source {i+1}")

                            st.write(doc.page_content[:1200])

                            st.write(
                                f"Similarity Score: {round(float(score), 4)}"
                            )

                            st.divider()

# =====================================================
# ABOUT PAGE
# =====================================================
elif page == "About":

    st.title("ℹ️ About")

    st.markdown("""
    ## GenAI Decision Intelligence Platform

    Advanced AI-powered conversational RAG platform.

    ### Technologies Used

    - Python
    - Streamlit
    - LangChain
    - Groq LLM
    - HuggingFace Embeddings
    - FAISS Vector Database
    - Retrieval-Augmented Generation (RAG)

    ### Features

    - Multi-PDF Upload
    - Conversational AI
    - Semantic Retrieval
    - Source Citations
    - Persistent Vector Storage
    - Downloadable AI Reports
    - Expert AI Modes
    - Explainable AI
    """)