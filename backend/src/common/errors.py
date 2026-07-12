from typing import Any, Dict, List, Optional


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: Optional[List[Any]] = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


class ValidationError(AppError):
    def __init__(self, message: str, details: Optional[List[Any]] = None) -> None:
        super().__init__("VALIDATION_ERROR", message, 400, details)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__("UNAUTHORIZED", message, 403)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__("NOT_FOUND", message, 404)


class OpenAIError(AppError):
    def __init__(self, message: str = "AI guidance unavailable") -> None:
        super().__init__("AI_UNAVAILABLE", message, 502)
