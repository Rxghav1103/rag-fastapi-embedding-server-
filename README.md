# Lightweight FastAPI Server for Retrieval-Augmented Generation (RAG)

This repository contains a lightweight FastAPI server for Retrieval-Augmented Generation (RAG). The server uses ChromaDB's persistent client for document ingestion and querying. It supports various document types, including PDF, DOC, DOCX, and TXT. Sentence embeddings are generated using the `sentence-transformers/all-MiniLM-L6-v2` model from Hugging Face, optimized for CPU usage. The API endpoints are non-blocking and handle concurrency efficiently.

## Features
- **Document Ingestion and Querying**: Ingest and query documents (PDF, DOC, DOCX, TXT) using ChromaDB.
- **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` for generating document embeddings.
- **Non-blocking API**: Efficient handling of concurrent requests using FastAPI.

## Tech Stack
- **FastAPI**: For building API endpoints.
- **ChromaDB**: To store and query document embeddings.
- **Sentence-Transformers**: For generating embeddings using `all-MiniLM-L6-v2`.
- **Python**: General-purpose programming.
- **Uvicorn**: ASGI server for running the FastAPI app.

## Libraries and Technologies Used
1. **FastAPI**: A modern, fast (high-performance) web framework for building APIs in Python.
2. **Uvicorn**: A lightning-fast ASGI server for running the FastAPI application.
3. **ChromaDB**: A vector database used for storing and querying embeddings.
4. **Sentence-Transformers**: A library for sentence and text embeddings using transformers.
5. **langchain**: To load and process different types of documents.
6. **Python Standard Libraries**: Libraries like `uuid` for unique ID generation and `logging` for logging.

## Getting Started
### Prerequisites
- Python 3.8+
- `pip` for package installation

### Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/<username>/lightweight-fastapi-rag-server.git
   cd lightweight-fastapi-rag-server
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```sh
   uvicorn main:app --reload
   ```
   The server will start at `http://127.0.0.1:8000`.

## API Endpoints
### 1. `/ingest/` [POST]
Ingest documents (PDF, DOC, DOCX, TXT) for future retrieval.
- **Request**: Multipart form containing files to ingest.
- **Example Input**: Upload files via Postman or Thunder Client.
  - **Input**: `sample1.txt`, `sample2.pdf`
- **Example Response**:
  ```json
  {
    "status": "Documents ingested successfully"
  }
  ```

### 2. `/query/` [GET]
Query the ingested documents.
- **Parameters**: `query` (str) - Text query to search the documents.
- **Example Input**:
  - **URL**: `http://127.0.0.1:8000/query/?query=What is FastAPI?`
- **Example Response**:
  ```json
  {
    "results": [
      {
        "filename": "sample1.txt",
        "score": 0.7214248776435852,
        "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+..."
      }
    ]
  }
  ```

### 3. `/database/` [GET]
Retrieve all ingested documents.
- **Response**: JSON with all documents' metadata and text.
- **Example Response**:
  ```json
  {
    "documents": [
      {
        "filename": "sample1.txt",
        "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, fast (high-performance), web framework for building APIs..."
      },
      {
        "filename": "sample2.pdf",
        "text": "This is a sample PDF document..."
      }
    ]
  }
  ```

## Running the Server
1. **Start the Server**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - The `--reload` flag allows automatic restart when changes are detected.
   - The server will be accessible at `http://localhost:8000`.

2. **Testing Endpoints**
   - Use tools like **Postman**, **Thunder Client**, or simply a web browser to interact with the endpoints.

## Usage Example
### Ingest Documents
Use tools like Postman or Thunder Client to POST documents to `/ingest/`.
- **Request**: Select `POST` method, use the URL `http://localhost:8000/ingest/`, and add files in the form-data section.

### Query Documents
Send a GET request to `/query/` with the desired query string.
- **Request**: Select `GET` method, use the URL `http://localhost:8000/query/?query=<your_query>`.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

For any questions, feel free to reach out to me at [raghavendra.bhargava2004@gmail.com](mailto:raghavendra.bhargava2004@gmail.com) or visit my GitHub: [Rxghav1103](https://github.com/Rxghav1103).

## License
This project is licensed under the MIT License.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Sentence-Transformers](https://www.sbert.net/)
- [Langchain](https://langchain.com/)
