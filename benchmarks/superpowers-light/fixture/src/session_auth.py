import random
import time


def create_session(user_id: int) -> dict[str, int | str]:
    generator = random.Random(user_id)
    token = f"{generator.getrandbits(128):032x}"
    return {"token": token, "created_at": int(time.time())}


def is_session_valid(session: dict[str, int | str]) -> bool:
    return bool(session.get("token"))
