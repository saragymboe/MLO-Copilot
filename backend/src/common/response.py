import uuid
from typing import Any, Dict


def build_success_response(data: Any, request_id: str | None = None) -> Dict[str, Any]:
    return {"success": True, "data": data, "requestId": request_id or str(uuid.uuid4())}


def build_error_response(code: str, message: str, request_id: str | None = None, details: list[Any] | None = None) -> Dict[str, Any]:
    return {"success": False, "error": {"code": code, "message": message, "details": details or []}, "requestId": request_id or str(uuid.uuid4())}
