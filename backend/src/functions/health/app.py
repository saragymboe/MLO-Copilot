import json
from common.response import build_success_response


def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(build_success_response({"status": "ok"})),
    }
