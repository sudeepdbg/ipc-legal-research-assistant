from sentence_transformers import SentenceTransformer, CrossEncoder
import os
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

class LegalRetriever:
    def __init__(self, chroma_path=None, collection_name="legal_docs",
                 embed_model_name='all-MiniLM-L6-v2',
                 rerank_model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        # If no path is provided, use a path relative to this file's location
        if chroma_path is None:
            # Get the directory of this file (retriever.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the project root
            project_root = os.path.dirname(current_dir)
            chroma_path = os.path.join(project_root, "chroma_db")
        self.embed_model = SentenceTransformer(embed_model_name)
        self.reranker = CrossEncoder(rerank_model_name)
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_collection(collection_name)

    def retrieve(self, query, top_k=20, rerank_top_k=5):
        # 1. Embed query
        query_emb = self.embed_model.encode(query).tolist()
        # 2. Initial search
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        docs = results['documents'][0]
        metas = results['metadatas'][0]

        if not docs:
            return []

        # 3. Rerank
        pairs = [[query, doc] for doc in docs]
        scores = self.reranker.predict(pairs)
        # Sort by score descending
        scored = sorted(zip(scores, docs, metas), key=lambda x: x[0], reverse=True)
        top = scored[:rerank_top_k]
        return [{"document": doc, "metadata": meta, "score": score} for score, doc, meta in top]
