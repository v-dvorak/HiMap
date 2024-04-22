from pathlib import Path

API_KEY_FILE = "api_key.txt"


def load_api_key() -> str:
    """
    :return: saved API key
    """
    api_key_file = Path(API_KEY_FILE)
    if api_key_file.is_file():
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
        if is_valid_api_key(api_key):
            return api_key
    raise FileNotFoundError("API key file not found or invalid")


def is_valid_api_key(api_key: str) -> bool:
    """
    Checks if API key is valid

    :param api_key: API key
    :return: True if the API key is valid, False otherwise
    """
    return len(api_key) > 0


def save_api_key(api_key: str) -> None:
    """
    Saves API key

    :param api_key: API key
    """
    api_key_file = Path(API_KEY_FILE)
    with open(api_key_file, "w") as f:
        f.write(api_key)
