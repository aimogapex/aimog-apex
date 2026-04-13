from dataclasses import dataclass
import os


@dataclass
class Settings:
    azure_openai_endpoint: str
    azure_openai_deployment_name: str
    azure_openai_api_key: str
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            azure_openai_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            log_level=os.getenv("SYNTHESIS_INSIGHT_LOG_LEVEL", "INFO"),
        )