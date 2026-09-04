import json
from pathlib import Path
from models import Challenge

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "challenges.json"

def load_challenges():
    return [Challenge.model_validate(x) for x in json.loads(DATA_FILE.read_text(encoding="utf-8"))]

def get_challenge(challenge_id):
    for c in load_challenges():
        if c.id == challenge_id:
            return c
    raise ValueError(f"Unknown challenge: {challenge_id}")
