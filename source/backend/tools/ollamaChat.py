from langchain_ollama import ChatOllama

def create_ollama_chat(model: str = "llama3", base_url: str = "http://localhost:11434", temperature: float = 0.2, max_tokens: int = 200):
    """
    Crée une instance ChatOllama pour interagir avec une instance Ollama locale.
    Args:
        model: Nom du modèle Ollama (ex: "llama3", "mistral", "phi3", etc.)
        base_url: URL de l'instance Ollama locale
        temperature: Température du modèle
        max_tokens: Nombre maximum de tokens générés
    Returns:
        ChatOllama: Instance du modèle de chat
    """
    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )
