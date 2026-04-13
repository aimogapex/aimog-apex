import requests
from .config import Settings


class AzureChatClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def chat(self, messages: list[dict]) -> str:
        url = (
            f"{self._settings.azure_openai_endpoint}"
            f"/openai/deployments/{self._settings.azure_openai_deployment_name}"
            "/chat/completions?api-version=2024-02-15-preview"
        )

        headers = {
            "Content-Type": "application/json",
            "api-key": self._settings.azure_openai_api_key,
        }

        payload = {
            "messages": messages,
            "temperature": 0.2,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]