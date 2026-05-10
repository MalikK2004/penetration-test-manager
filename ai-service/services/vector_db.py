import os

class VectorDBService:
    def __init__(self):
        self.enabled = os.getenv("ENABLE_RAG", "false").lower() == "true"
        # Stub for chromadb / pinecone
        self.collection = None

    def store_finding(self, finding_id, text, metadata=None):
        if not self.enabled: return
        # Stub: store embedding in vector DB
        pass

    def retrieve_similar(self, query, top_k=3):
        if not self.enabled: return []
        # Stub: return similar historical findings
        return []

vector_db = VectorDBService()
