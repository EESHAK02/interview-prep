import json
import os

SESSION_FILE = "data/sessions.json"
WEAKNESS_FILE = "data/weaknesses.json"


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def log_session(entry):
    sessions = load_json(SESSION_FILE, [])
    sessions.append(entry)
    save_json(SESSION_FILE, sessions)


def log_weakness(weakness):
    weaknesses = load_json(WEAKNESS_FILE, [])
    weaknesses.append(weakness)
    save_json(WEAKNESS_FILE, weaknesses)
