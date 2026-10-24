import os


def get_model_client():
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if provider == "ollama":
        from models.ollama_client import send_message
        return send_message

    elif provider == "mock":
        from models.mock_client import send_message
        return send_message

    else:
        raise ValueError(
            f"Неизвестный AI_PROVIDER: {provider}. "
            "Доступные варианты: ollama, mock."
        )
