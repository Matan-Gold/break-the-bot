"""משווה את קצב השבירה של החוקים השבירים בין רמה 1 לרמה 2 (אותו מודל, פרומפט שונה).

הרצה: .venv/Scripts/python.exe -X utf8 tests/compare_levels.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app  # noqa: E402
from run_break_tests import SCENARIOS, classify  # noqa: E402

PACE = 2.5
K = 2
BREAKABLE = [sc for sc in SCENARIOS if sc["expect"] == "breakable"]


def run(turns, prompt):
    history, replies = [], []
    for user_msg in turns:
        history.append({"role": "user", "content": user_msg})
        try:
            r = app.get_model_reply(history, prompt)
        except Exception as e:  # noqa: BLE001
            r = f"[err {e}]"
        time.sleep(PACE)
        history.append({"role": "assistant", "content": r})
        replies.append(r)
    return replies


def break_rate(sc, prompt):
    broke = 0
    for _ in range(K):
        replies = run(sc["turns"], prompt)
        if classify(sc["rule"], replies) == "BROKE":
            broke += 1
    return broke


if __name__ == "__main__":
    os.environ.setdefault("HF_TOKEN", app.get_token() or "")
    print(f"השוואת רמות (K={K} לכל תרחיש)\n")
    print(f"{'חוק':>4} {'תרחיש':<34} {'רמה1':>6} {'רמה2':>6}")
    print("-" * 56)
    for sc in BREAKABLE:
        l1 = break_rate(sc, app.LEVELS[1]["prompt"])
        l2 = break_rate(sc, app.LEVELS[2]["prompt"])
        print(f"{sc['rule']:>4} {sc['label']:<34} {l1}/{K:<5} {l2}/{K:<5}")
