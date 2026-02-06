# Ragume - Portfolio RAG Chatbot

![Vibe Code](https://img.shields.io/badge/Vibe-Coding-purple?style=for-the-badge&logo=sparkles)

Welcome to **Ragume**, a "vibe code" project that turns a portfolio into an interactive RAG (Retrieval-Augmented Generation) chatbot. This project allows users to chat with a portfolio assistant to learn about the candidate's skills, experience, and projects.

## 🚀 Features

-   **RAG Agent**: Intelligent chatbot powered by LangChain and OpenAI.
-   **Vector Search**: Uses Milvus for efficient document retrieval.
-   **Semantic Cache**: Built-in semantic caching layer that stores and instantly retrieves responses for similar queries, significantly reducing latency and API costs.
-   **Streamlit UI**: A "jazzy" interface for interacting with the agent.
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
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### Frontend (Streamlit)
In a separate terminal, start the Streamlit UI:
```bash
streamlit run ui.py
```
The UI will open in your browser at `http://localhost:8501`.

## 🔌 API Endpoints

The backend provides the following endpoints:

### Core Endpoints

-   **`POST /agent`**
    -   **Description**: Runs the RAG agent to answer a question.
    -   **Input**: JSON body with `message` (string).
    -   **Rate Limit**: 10 requests/minute.
    -   **Response**: `{"response": "...", "source": "live/cache"}`

-   **`POST /ingest`**
    -   **Description**: Ingests a PDF file into the vector store.
    -   **Input**: JSON body with `file_path` (string).
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

-   `vpython.bat`: A wrapper script to run Python commands within the virtual environment (Windows only).
    -   Example: `vpython.bat run_script.py`
