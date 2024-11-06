from fastapi import FastAPI, UploadFile, File
import uvicorn
from chromadb import Client as ChromaClient
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SentenceTransformer model (CPU)
try:
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer model: {str(e)}")
    raise e

# Configure ChromaDB client for persistence
try:
    chroma_client = ChromaClient()
    collection = chroma_client.get_or_create_collection(name="documents")
    logger.info("ChromaDB client initialized and collection created successfully.")
except Exception as e:
    logger.error(f"Error initializing ChromaDB client: {str(e)}")
    raise e

@app.post("/ingest/", response_class=JSONResponse)
async def ingest_documents(files: List[UploadFile] = File(...)):
    """ Endpoint to ingest documents for retrieval """
    documents = []
    embeddings = []
    ids = []
    
    try:
        # Read files and prepare documents
        for file in files:
            try:
                content = await file.read()
                text = content.decode('utf-8')
                doc_id = str(uuid.uuid4())
                doc = {"text": text, "metadata": {'filename': file.filename}}
                documents.append(doc)
                ids.append(doc_id)
                logger.info(f"File '{file.filename}' read successfully.")
            except UnicodeDecodeError:
                logger.error(f"Failed to decode file '{file.filename}'. Unsupported characters.")
                return JSONResponse(content={"error": f"Failed to decode '{file.filename}'. Unsupported characters."}, status_code=400)
            except Exception as e:
                logger.error(f"Error reading file '{file.filename}': {str(e)}")
                return JSONResponse(content={"error": f"Error reading file '{file.filename}': {str(e)}"}, status_code=500)

        # Perform embedding for documents
        try:
            embeddings = [model.encode(doc["text"]).tolist() for doc in documents]
            logger.info("Embeddings generated successfully.")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return JSONResponse(content={"error": f"Error generating embeddings: {str(e)}"}, status_code=500)

        # Add documents to ChromaDB
        try:
            collection.add(ids=ids, documents=[doc["text"] for doc in documents], metadatas=[doc["metadata"] for doc in documents], embeddings=embeddings)
            logger.info("Documents added to ChromaDB successfully.")
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {str(e)}")
            return JSONResponse(content={"error": f"Error adding documents to database: {str(e)}"}, status_code=500)

        return JSONResponse(content={"status": "Documents ingested successfully"})

    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {str(e)}")
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)

@app.get("/query/", response_class=JSONResponse)
async def query_document(query: str):
    """ Endpoint to query documents """
    try:
        # Generate embedding for the query
        query_embedding = model.encode(query).tolist()
        logger.info("Query embedding generated successfully.")
        
        # Query ChromaDB
        results = collection.query(query_embeddings=[query_embedding], n_results=5)
        response = [
            {
                "filename": metadata.get('filename', 'unknown') if isinstance(metadata, dict) else 'unknown',
                "score": distance,
                "text": document
            }
            for metadata, distance, document in zip(results['metadatas'], results['distances'], results['documents'])
        ]
        logger.info("Query executed successfully.")
        return JSONResponse(content={"results": response})
    
    except Exception as e:
        logger.error(f"Error during query: {str(e)}")
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)

@app.get("/database/", response_class=JSONResponse)
async def get_database():
    """ Endpoint to view all documents in the database """
    try:
        documents = collection.get()
        response = [
            {
                "filename": metadata.get('filename', 'unknown') if isinstance(metadata, dict) else 'unknown',
                "text": document
            }
            for metadata, document in zip(documents['metadatas'], documents['documents'])
        ]
        logger.info("Retrieved all documents from the database successfully.")
        return JSONResponse(content={"documents": response})
    except Exception as e:
        logger.error(f"Error retrieving documents from database: {str(e)}")
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    # Ensure the database is consistent and persists across sessions
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

