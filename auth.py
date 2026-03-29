from jose import jwt
from datetime import UTC, datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(UTC) + timedelta(hours=1)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)