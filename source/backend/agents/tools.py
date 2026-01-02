"""Agent tools for document retrieval and processing"""
from tools.rag_system import RAGSystem


class RAGRetrieverTool:
    """Wrapper for RAG system to use as an agent tool"""
    
    def __init__(self, persist_directory: str = "../database/prod"):
        self.rag_system = RAGSystem(persist_directory=persist_directory)
    
    def retrieve(self, question: str, k: int = 6) -> list:
        """Retrieve relevant documents for a question
        
        Args:
            question: The user's question
            k: Number of documents to retrieve (Note: currently fixed at 6 in RAGSystem)
            
        Returns:
            List of document objects with page_content and metadata
        """
        retriever = self.rag_system.get_retriever()
        docs = retriever.invoke(question)
        return docs
    
    def format_docs(self, docs: list) -> str:
        """Format retrieved documents into a string context
        
        Args:
            docs: List of document objects
            
        Returns:
            Formatted string with all document contents
        """
        return "\n\n".join(
            f"Document {i+1} (ID: {doc.metadata.get('id', 'N/A')}):\n{doc.page_content}" 
            for i, doc in enumerate(docs)
        )
