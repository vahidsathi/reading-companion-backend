import json
from pathlib import Path
from app.db.session import SessionLocal
from app.models.passage import Passage

DATA_DIR = Path("data/passages")

def load_file(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("Current working directory:", Path.cwd())
    print("Looking for passages in:", DATA_DIR.resolve())

    files = list(DATA_DIR.glob("*.json"))
    print("Found JSON files:", [f.name for f in files])

    db = SessionLocal()
    added = 0

    for file in files:
        data = load_file(file)
        print(f"{file.name}: {len(data)} passages")
        for item in data:
            passage = Passage(
                grade=item["grade"],
                passage_code=item["passage_code"],
                title=item["title"],
                text=item["text"],
            )
            db.add(passage)
            added += 1

    db.commit()
    db.close()
    print("Passages loaded. Inserted:", added)

if __name__ == "__main__":
    main()
