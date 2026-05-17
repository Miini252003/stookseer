from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple


class AuthManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_store()

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _ensure_store(self) -> None:
        if self.db_path.exists():
            return
        default_admin = {
            "admin": {
                "password": self.hash_password("admin123"),
                "name": "Admin User",
            }
        }
        self.db_path.write_text(json.dumps(default_admin, indent=2), encoding="utf-8")

    def _load_users(self) -> Dict[str, Dict[str, str]]:
        raw = self.db_path.read_text(encoding="utf-8")
        return json.loads(raw or "{}")

    def _save_users(self, users: Dict[str, Dict[str, str]]) -> None:
        self.db_path.write_text(json.dumps(users, indent=2), encoding="utf-8")

    def register_user(self, username: str, password: str, name: str) -> Tuple[bool, str]:
        users = self._load_users()
        if username in users:
            return False, "User already exists."

        users[username] = {
            "password": self.hash_password(password),
            "name": name,
        }
        self._save_users(users)
        return True, "User registered successfully."

    def validate_user(self, username: str, password: str):
        users = self._load_users()
        profile = users.get(username)
        if not profile:
            return False, {}
        if profile.get("password") != self.hash_password(password):
            return False, {}
        return True, profile
