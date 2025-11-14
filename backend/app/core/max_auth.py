"""
Max Authentication
Utilities for verifying Max Mini App init data.
"""

# --------------------------------------------------------------------------------

import hashlib
import hmac
import json
import time
import urllib.parse
from typing import Any, Optional

# --------------------------------------------------------------------------------


def verify_init_data_and_get_user_id(
    init_data_raw: str, bot_token: str, max_age_sec: int = 900
) -> Optional[dict[str, Any]]:
    """
    Verify Max Mini App init data and extract user information.

    Args:
        init_data_raw: Raw init data from Max
        bot_token: Bot token for verification
        max_age_sec: Maximum age of init data in seconds (default: 15 minutes)

    Returns:
        Dict with user_id and user data if valid, None otherwise
    """
    try:
        parsed = urllib.parse.parse_qs(init_data_raw, strict_parsing=True)
        received_hash = parsed.pop("hash")[0]

        pairs = [f"{k}={v[0]}" for k, v in parsed.items()]
        pairs.sort()
        data_check_string = "\n".join(pairs)

        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(calc_hash, received_hash):
            return None

        auth_date = int(parsed["auth_date"][0])
        if abs(time.time() - auth_date) > max_age_sec:
            return None

        user = json.loads(parsed["user"][0])
        return {"user_id": user["id"], "user": user}

    except Exception:
        return None


def extract_max_auth_from_header(auth_header: str) -> Optional[str]:
    """
    Extract init data from Authorization header.

    Args:
        auth_header: Authorization header value

    Returns:
        Init data string if valid format, None otherwise
    """
    if not auth_header or not auth_header.startswith("tma "):
        return None

    return auth_header[4:]  # Remove "tma " prefix
