from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

class LegalRetriever:
    def __init__(self, chroma_path="chroma_db", collection_name="legal_docs",
                 embed_model_name='all-MiniLM-L6-v2',
                 rerank_model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        # Embedding model
        self.embed_model = SentenceTransformer(embed_model_name)
        # Reranker
        self.reranker = CrossEncoder(rerank_model_name)
        # Chroma client
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
