
import base64
import json

def generate_wheely_signature(token: str) -> str:
    """
    Mimics the JS function:
    m = (e) => btoa(JSON.stringify({ type: "captcha", signature: e }));
    """
    payload = {
        "type": "captcha",
        "signature": token
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()
