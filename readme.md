# 🧠 GenAI Decision Intelligence Platform

### Developed by Vatsal Bhimsariya

🚀 Live Demo: [https://genai-decision-intelligence-platform.streamlit.app/](https://genai-decision-intelligence-platform.streamlit.app/)

---

# 📌 Overview

GenAI Decision Intelligence Platform is an advanced AI-powered conversational RAG (Retrieval-Augmented Generation) system designed for intelligent document understanding and contextual reasoning.

The platform allows users to upload multiple PDF documents and interact with them using conversational AI. It combines semantic retrieval, vector databases, conversational memory, and expert analysis modes to generate accurate and explainable responses.

This project demonstrates modern GenAI engineering concepts including:

* Conversational AI
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Prompt Engineering
* Multi-Document Intelligence
* Persistent Vector Storage
* Explainable AI

---

# 🚀 Live Application

🔗 [https://genai-decision-intelligence-platform.streamlit.app/](https://genai-decision-intelligence-platform.streamlit.app/)

---

# ✨ Features

## 📄 Multi-PDF Upload

Upload and process multiple PDF documents simultaneously.

## 💬 Conversational AI Interface

ChatGPT-style conversational UI for natural interaction.

## 🔍 Semantic Search

Uses embeddings and vector similarity search to retrieve relevant contextual information.

## 🧠 Retrieval-Augmented Generation (RAG)

Combines retrieved document context with LLM reasoning for grounded responses.

## 🗂️ Vector Database

FAISS vector database for efficient semantic retrieval.

## 📚 Source Citations

Displays retrieved document chunks and similarity scores for explainability.

## 💾 Persistent Vector Storage

Stores vector indexes locally for reuse across sessions.

## 🎯 Expert AI Modes

Supports multiple intelligent assistant modes:

* General Assistant
* Business Analyst
* Research Assistant
* Resume Reviewer
* Financial Advisor

## 📥 Downloadable AI Reports

Generate downloadable AI-generated analysis reports.

## 🧠 Conversational Memory

Maintains context-aware interactions using session memory.

---

# 🏗️ System Architecture

```text
User Query
    ↓
Streamlit Frontend
    ↓
Conversational RAG Pipeline
    ↓
Semantic Retrieval (FAISS)
    ↓
Relevant Document Chunks
    ↓
Groq LLM Processing
    ↓
Context-Aware AI Response
```

---

# ⚙️ Tech Stack

| Category               | Technologies          |
| ---------------------- | --------------------- |
| Programming Language   | Python                |
| Frontend/UI            | Streamlit             |
| LLM Framework          | LangChain             |
| LLM Provider           | Groq                  |
| Embeddings             | Sentence Transformers |
| Vector Database        | FAISS                 |
| PDF Processing         | PyPDF                 |
| Environment Management | Python Dotenv         |

---

# 🧠 AI Concepts Implemented

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Embeddings
* Vector Similarity Search
* Conversational Memory
* Prompt Engineering
* Explainable AI
* Contextual Reasoning
* Multi-Document Intelligence

---

# 📂 Project Structure

```text
GenAI-Decision-Platform/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── vector_store/
```

---

# 🛠️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/vatsalbhimsariya/genai-decision-intelligence-platform.git
```

## 2️⃣ Open Project Folder

```bash
cd genai-decision-intelligence-platform
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Create .env File

```env
GROQ_API_KEY=your_groq_api_key
```

## 5️⃣ Run Application

```bash
streamlit run app.py
```

---

# 🎯 Future Improvements

Potential future upgrades:

* FastAPI Backend
* Cloud Vector Database
* User Authentication
* Multi-Agent AI Systems
* AI Evaluation Metrics
* Analytics Dashboard
* Streaming Responses
* Docker Deployment

---

# 💡 Interview Highlights

This project can be used to discuss:

* RAG architecture
* Embeddings and semantic retrieval
* Vector databases
* Conversational AI systems
* Prompt engineering
* Explainable AI
* Context-aware reasoning
* Production deployment

---

# 👨‍💻 Developer

## Vatsal Bhimsariya

* GitHub: [https://github.com/vatsalbhimsariya](https://github.com/vatsalbhimsariya)
* Live Project: [https://genai-decision-intelligence-platform.streamlit.app/](https://genai-decision-intelligence-platform.streamlit.app/)

---

# ⭐ Conclusion

This project demonstrates the development of a modern production-style GenAI application integrating conversational AI, semantic retrieval, and explainable document intelligence.

It reflects practical implementation of advanced AI engineering concepts beyond traditional beginner machine learning projects.
