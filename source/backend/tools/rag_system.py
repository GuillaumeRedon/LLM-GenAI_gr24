from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from datetime import datetime
from typing import List
import os
import uuid

from tools.document_loader import build_document_from_fields

class RAGSystem:
    """ RAG System with Chroma and HuggingFace embeddings"""

    def __init__(
        self,
        documents: List[Document]=None,
        persist_directory: str="",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        """
        Initializes the RAG system.
        
        Args:
            documents: List of documents to index
            persist_directory: Directory to persist the Chroma database
            embedding_model: Embedding model (multilingual for French)
        """
        self.persist_directory = persist_directory
        
        # Initialize embeddings (multilingual model for French)
        print(f"Loading embedding model: {embedding_model} ...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embedding model loaded")
        
        # Create or load the Chroma vector store
        # Check if the store already exists with data
        db_exists = False
        if os.path.exists(persist_directory):
            try:
                # Try to load an existing store
                test_store = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=self.embeddings
                )
                # Check if it contains documents
                if test_store._collection.count() > 0:
                    db_exists = True
                    self.vectorstore = test_store
                    print(f"Vector store loaded from {persist_directory} ({test_store._collection.count()} documents)")
            except:
                db_exists = False
        
        if not db_exists:
            if documents is None:
                raise ValueError("No documents provided to initialize the vector store.")
            print(f"Creating vector store with {len(documents)} documents...")
            print("   This may take a few minutes to generate embeddings...")
            
            # Create the directory if it doesn't exist
            os.makedirs(persist_directory, exist_ok=True)
            
            # Create the vector store and persist it
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=persist_directory
            )
            
            print(f"Vector store created and saved in {persist_directory}")
        
        # Create the retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 6}  # Return the 6 most similar documents
        )
    
    def get_retriever(self):
        """Return the retriever for use in a RAG chain"""
        return self.retriever
    
    def add_question(
        self,
        titre: str,
        contenu: str,
        thematique: str,
        ecoles: str,
        utilisateurs: str,
        langue: str,
        date: str = datetime.now().strftime("%Y-%m-%d"),
        post_type: str = "",
        status: str = ""
    ):
        """
        Adds or updates a question in the vector store.
        """
        generated_id = str(uuid.uuid4())
        doc = build_document_from_fields(
            question_id=generated_id,
            titre=titre,
            contenu=contenu,
            thematique=thematique,
            ecoles=ecoles,
            utilisateurs=utilisateurs,
            langue=langue,
            date=date,
            post_type=post_type,
            status=status,
        )

        doc_id = generated_id

        # Remove an old document with the same ID if present
        try:
            self.vectorstore.delete(ids=[doc_id])
        except Exception:
            pass  # The ID did not exist yet
        self.vectorstore.add_documents([doc], ids=[doc_id])
        #self.vectorstore.persist()