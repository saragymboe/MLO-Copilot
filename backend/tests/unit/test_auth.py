from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common.auth import get_caller_identity, is_admin


def test_get_caller_identity_extracts_groups():
    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "user-1", "email": "user@example.com", "cognito:groups": "Admins,Users"}}}}}
    identity = get_caller_identity(event)
    assert identity["sub"] == "user-1"
    assert identity["email"] == "user@example.com"
    assert identity["groups"] == ["Admins", "Users"]


def test_is_admin_detects_admin_group():
    event = {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": "user-1", "cognito:groups": "Admins"}}}}}
    assert is_admin(event) is True
