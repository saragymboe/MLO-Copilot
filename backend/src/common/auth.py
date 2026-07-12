from typing import Any, Dict, List


class AuthError(Exception):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message)
        self.message = message


def get_caller_identity(event: Dict[str, Any]) -> Dict[str, Any]:
    request_context = event.get("requestContext", {})
    authorizer = request_context.get("authorizer") or {}
    jwt = authorizer.get("jwt") or {}
    claims = jwt.get("claims") or {}
    groups = []
    if claims.get("cognito:groups"):
        groups = [group.strip() for group in claims.get("cognito:groups", "").split(",") if group.strip()]
    return {
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "groups": groups,
        "issuer": claims.get("iss"),
        "token_use": claims.get("token_use"),
    }


def require_auth(event: Dict[str, Any]) -> Dict[str, Any]:
    identity = get_caller_identity(event)
    if not identity.get("sub"):
        raise AuthError("Authentication required")
    return identity


def is_admin(event: Dict[str, Any]) -> bool:
    return "Admins" in get_caller_identity(event).get("groups", [])
