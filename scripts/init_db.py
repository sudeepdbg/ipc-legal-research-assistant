import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from data_loader import load_ipc_sections, load_judgments

# Configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "legal_docs"

# Initialize embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Load data
ipc_chunks, ipc_metas = load_ipc_sections("data/ipc_sections.csv")
judgment_chunks, judgment_metas = load_judgments("data/judgments/")  # optional

all_chunks = ipc_chunks + judgment_chunks
all_metas = ipc_metas + judgment_metas

# Generate embeddings
print(f"Generating embeddings for {len(all_chunks)} chunks...")
embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()

# Initialize ChromaDB client (persistent)
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create or get collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Add data to collection
ids = [str(i) for i in range(len(all_chunks))]
collection.add(
    embeddings=embeddings,
    documents=all_chunks,
    metadatas=all_metas,
    ids=ids
)

print("Vector database built successfully.")
