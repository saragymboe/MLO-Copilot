import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Config:
    stage: str = os.getenv("STAGE", "dev")
    table_name: str = os.getenv("DYNAMODB_TABLE_NAME", "MortgageProductCopilot-dev")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    openai_secret_arn: Optional[str] = os.getenv("OPENAI_SECRET_ARN")
    openai_timeout_seconds: int = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "20"))
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "https://example.amplifyapp.com")
    region: str = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


CONFIG = Config()
