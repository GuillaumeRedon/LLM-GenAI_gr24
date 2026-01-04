"""Agent tools for document retrieval and processing"""
from tools.rag_system import RAGSystem


class RAGRetrieverTool:
    """Wrapper for RAG system to use as an agent tool"""
    
    def __init__(self, persist_directory: str = "../database/prod", k_docs: int = 6):
        self.rag_system = RAGSystem(persist_directory=persist_directory, k_docs=k_docs)
    
    def retrieve(self, question: str) -> list:
        """Retrieve relevant documents for a question
        
        Args:
            question: The user's question
            
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
