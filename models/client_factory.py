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


def get_model_client():
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()

    if provider == "ollama":
        from models.ollama_client import send_message
        return send_message

    elif provider == "mock":
        from models.mock_client import send_message
        return send_message

    elif provider == "cloud":
        from models.cloud_client import send_message
        return send_message

    else:
        raise ValueError(
            f"Неизвестный AI_PROVIDER: {provider}. "
            "Доступные варианты: ollama, mock, cloud."
        )


def list_models():
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()
    if provider == "ollama":
        from models.ollama_client import list_models as get_list
        return get_list()
    elif provider == "cloud":
        from models.cloud_client import list_models as get_list
        return get_list()
    return ["mock-model"]


def set_model(model_name: str):
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()
    if provider == "ollama":
        from models.ollama_client import set_model as change_model
        return change_model(model_name)
    elif provider == "cloud":
        from models.cloud_client import set_model as change_model
        return change_model(model_name)
    return model_name


def get_current_model():
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()
    if provider == "ollama":
        from models.ollama_client import get_current_model as current
        return current()
    elif provider == "cloud":
        from models.cloud_client import get_current_model as current
        return current()
    return "mock-model"
