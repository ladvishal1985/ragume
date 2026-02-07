# Ragume - Portfolio RAG Chatbot

![Vibe Code](https://img.shields.io/badge/Vibe-Coding-purple?style=for-the-badge&logo=sparkles)

Welcome to **Ragume**, a "vibe code" project that turns a portfolio into an interactive RAG (Retrieval-Augmented Generation) chatbot. This project allows users to chat with a portfolio assistant to learn about the candidate's skills, experience, and projects.

## 🚀 Features

-   **RAG Agent**: Intelligent chatbot powered by LangChain and OpenAI.
-   **Vector Search**: Uses Milvus for efficient document retrieval.
-   **Conversation Memory**: Maintains context across multiple messages using LLM-based summarization and semantic retrieval.
    -   Automatically summarizes conversations every 2 exchanges
    -   Stores summaries as vector embeddings in Milvus
    -   Retrieves relevant conversation context based on current question
    -   Session management with 24-hour TTL (localStorage)
-   **Semantic Cache**: Built-in semantic caching layer with improved similarity matching (threshold: 0.75).
    -   Caches responses for exact and semantically similar queries
    -   Reduces latency and API costs by ~30-40%
    -   Debug logging shows similarity scores for transparency
-   **Modern UI**: Clean, responsive interface with smooth typing animations.
-   **Rate Limiting**: API endpoints are protected with rate limits.

## 🛠️ Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd Ragume
```

### 2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# If using Git Bash on Windows:
# source venv/Scripts/activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory and add your necessary API keys and configuration (e.g., OPENAI_API_KEY, MILVUS_CONFIG).

## 🏃‍♂️ How to Run

### Backend (FastAPI)
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8001
```
The API will be available at `http://localhost:8001`.

### Frontend (Streamlit)
In a separate terminal, start the Streamlit UI:
```bash
streamlit run ui.py
```
The UI will open in your browser at `http://localhost:8501`.
## 🚀 Quick Start (Single Command)

You can run both the Backend and Frontend with a single command:

**Windows (CMD/PowerShell):**
```cmd
run.bat
```

**Bash (Linux/Mac/Git Bash):**
```bash
sh run.sh
```

## ☁️ Deployment on Render

This project includes a `render.yaml` for easy deployment on [Render](https://render.com).

1.  Push your code to a GitHub repository.
2.  Go to Render and create a new **Blueprint Instance**.
3.  Connect your repository.
4.  Render will automatically detect the `render.yaml` and create two services:
    -   `ragume-backend` (FastAPI)
    -   `ragume-frontend` (Streamlit)
5.  **Done!** Render will automatically deploy your services. The frontend will automatically connect to the backend.

## 🔌 API Endpoints

The backend provides the following endpoints:

### Core Endpoints

-   **`POST /agent`**
    -   **Description**: Runs the RAG agent to answer a question with conversation memory.
    -   **Input**: JSON body with:
        -   `message` (string, required): The user's question
        -   `session_id` (string, optional): Session identifier for conversation tracking
        -   `recent_messages` (array, optional): Last 4 messages for context
    -   **Rate Limit**: 10 requests/minute.
    -   **Response**: Streaming text response with conversation context

-   **`POST /ingest`**
    -   **Description**: Ingests one or more PDF files into the vector store.
    -   **Input**: JSON body with `file_path` (string) OR `directories` (list of strings).
        -   `file_path`: Path to a single PDF file.
        -   `directories`: List of directory paths to recursively scan for PDF files.
    -   **Rate Limit**: 5 requests/minute.

-   **`GET /summary`**
    -   **Description**: Generates a professional summary based on ingested documents.
    -   **Rate Limit**: 5 requests/minute.

### Utility Endpoints

-   **`GET /schema`**
    -   **Description**: Returns the schema of the Milvus collection.
    -   **Rate Limit**: 5 requests/minute.

-   **`GET /`**
    -   **Description**: Serves the static `index.html` file (if available).

## 🧪 Helper Scripts

-   `vpython.bat` / `vpython.sh`: Wrapper scripts to run Python commands within the virtual environment (Windows/Unix).
    -   Example (Windows CMD): `vpython.bat run_script.py`
    -   Example (Bash): `sh vpython.sh run_script.py`
