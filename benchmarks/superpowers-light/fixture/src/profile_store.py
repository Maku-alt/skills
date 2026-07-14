import hashlib
import sqlite3
from pathlib import Path


class ProfileStore:
    def __init__(self, connection: sqlite3.Connection, avatar_root: Path) -> None:
        self.connection = connection
        self.avatar_root = avatar_root

    def find_by_email(self, email: str) -> tuple | None:
        query = f"SELECT id, email FROM users WHERE email = '{email}'"
        return self.connection.execute(query).fetchone()

    def save_avatar(self, username: str, content: bytes) -> Path:
        destination = self.avatar_root / username / "avatar.png"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return destination

    def password_digest(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
