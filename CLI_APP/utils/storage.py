from __future__ import annotations
import json
import os
from typing import List
from models.user import User

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def save_users(users: List[User]) -> None:
    _ensure_data_dir()
    payload = [u.to_dict() for u in users]
    with open(USERS_FILE, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)


def load_users() -> List[User]:
    _ensure_data_dir()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        return [User.from_dict(u) for u in payload]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"[warn] Could not parse data file: {exc}. Starting fresh.")
        return []


def find_user_by_email(users: List[User], email: str):
    email = email.strip().lower()
    for u in users:
        if u.email == email:
            return u
    return None


def find_user_by_id(users: List[User], user_id: int):
    for u in users:
        if u.id == user_id:
            return u
    return None