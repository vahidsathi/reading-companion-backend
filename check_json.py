import json
from pathlib import Path

files = sorted(Path("data/passages").glob("grade*.json"))
print("Checking:", files)

for f in files:
    try:
        json.load(open(f, "r", encoding="utf-8"))
        print("OK ", f)
    except Exception as e:
        print("BAD", f, e)
        break
