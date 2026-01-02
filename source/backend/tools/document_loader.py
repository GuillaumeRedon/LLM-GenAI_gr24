import json
from typing import List
from langchain_core.documents import Document

def build_document_from_fields(
    question_id: int,
    titre: str,
    contenu: str,
    thematique: str,
    ecoles: str,
    utilisateurs: str,
    langue: str,
    date: str = "",
    post_type: str = "",
    status: str = ""
) -> Document:
    """
    Builds a LangChain Document from individual fields
    respecting the existing format.
    """
    text_content = f"""[Écoles: {ecoles or 'N/A'}] [Thématique: {thematique or ''}]

Question: {titre}

Réponse: {contenu}"""

    metadata = {
        "id": question_id,
        "title": titre,
        "date": date,
        "post_type": post_type,
        "langues": langue,
        "thematiques": thematique,
        "utilisateurs": utilisateurs or "N/A",
        "ecoles": ecoles or "N/A",
        "status": status,
    }

    return Document(page_content=text_content, metadata=metadata)


def load_qa_documents(json_path: str) -> List[Document]:
    """
    Loads the Q&A documents from the JSON file.
    
    Args:
        json_path: Path to the QA_clean.json file
        
    Returns:
        List of LangChain Documents with metadata
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = []
    for item in data:
        # Create the enriched text content with important context
        ecoles = ', '.join(item.get('Écoles', [])) if item.get('Écoles', []) else 'N/A'
        thematiques = item.get('Thématiques', '')
        
        text_content = f"""[Écoles: {ecoles}] [Thématique: {thematiques}]

Question: {item.get('Title', '')}

Réponse: {item.get('Content', '')}"""
        
        # Create the metadata (for filtering and traceability)
        metadata = {
            'id': item.get('id'),
            'title': item.get('Title', ''),
            'date': item.get('Date', ''),
            'post_type': item.get('Post Type', ''),
            'langues': item.get('Langues', ''),
            'thematiques': item.get('Thématiques', ''),
            'utilisateurs': ', '.join(item.get('Utilisateurs', [])) if item.get('Utilisateurs', []) else 'N/A',
            'ecoles': ecoles,
            'status': item.get('Status', '')
        }

        # Create the LangChain document
        doc = Document(page_content=text_content, metadata=metadata)
        documents.append(doc)

    print(f"Loaded {len(documents)} documents from {json_path}")
    return documents
