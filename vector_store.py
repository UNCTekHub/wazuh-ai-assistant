# vector_store.py
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from document_processor import WazuhDocumentProcessor
import os

class WazuhVectorStore:
    def __init__(self, persist_directory="./wazuh_vector_store"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
    
    def create_vector_store(self, force_download=False):
        """Create vector store from Wazuh documents"""
        processor = WazuhDocumentProcessor()
        
        # Download documentation if forced or no docs exist
        if force_download or not os.path.exists(processor.docs_folder) or not os.listdir(processor.docs_folder):
            print("📥 No existing documentation found. Downloading...")
            if not processor.download_wazuh_documentation():
                raise Exception("Failed to download Wazuh documentation")
        
        # Load documents
        documents = processor.load_documents()
        if not documents:
            raise Exception("No documents found after download")
        
        # Split into chunks
        chunks = processor.chunk_documents(documents)
        print(f"🔨 Creating vector store with {len(chunks)} document chunks...")
        
        # Create vector store
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # Save locally
        self.vector_store.save_local(self.persist_directory)
        print(f"💾 Vector store saved to {self.persist_directory}")
        return len(chunks)
    
    def load_vector_store(self):
        """Load existing vector store"""
        if os.path.exists(self.persist_directory):
            try:
                self.vector_store = FAISS.load_local(
                    self.persist_directory, 
                    self.embeddings
                )
                print("📂 Vector store loaded successfully")
                return True
            except Exception as e:
                print(f"❌ Error loading vector store: {e}")
                return False
        return False
    
    def search_documents(self, query, k=5):
        """Search for relevant documents"""
        if self.vector_store is None:
            if not self.load_vector_store():
                raise ValueError("Vector store not found. Please create it first.")
        
        results = self.vector_store.similarity_search(query, k=k)
        print(f"🔍 Found {len(results)} relevant documents for query: '{query}'")
        return results

if __name__ == "__main__":
    vector_store = WazuhVectorStore()
    
    if not vector_store.load_vector_store():
        print("🆕 Creating new vector store...")
        vector_store.create_vector_store()
