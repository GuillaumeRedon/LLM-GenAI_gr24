from langchain_ollama import ChatOllama

def create_ollama_chat(model: str = "llama3", base_url: str = "http://localhost:11434", temperature: float = 0.2, max_tokens: int = 200):
    """
    Creates a ChatOllama instance to interact with a local Ollama instance.
    Args:
        model: Name of Ollama (ex: "llama3", "mistral", "phi3", etc.)
        base_url: URL of the local Ollama instance
        temperature: Model temperature
        max_tokens: Maximum number of generated tokens
    Returns:
        ChatOllama: Chat model instance
    """
    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )
