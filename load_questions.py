import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.question import Question
from app.models.passage import Passage

DATA_DIR = Path("data/questions")

def load_file(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    db = SessionLocal()
    files = list(DATA_DIR.glob("*.json"))
    if not files:
        print("No question files found in data/questions")
        db.close()
        return

    inserted = 0
    skipped = 0

    for file in files:
        data = load_file(file)

        for item in data:
            code = item["passage_code"].strip()
            passage = db.execute(
                select(Passage).where(Passage.passage_code == code).limit(1)
            ).scalars().first()

            if not passage:
                print(f"Skipping: passage_code not found: {code}")
                skipped += 1
                continue

            q = Question(
                passage_id=passage.id,
                prompt=item["prompt"],
                choice_a=item["choice_a"],
                choice_b=item["choice_b"],
                choice_c=item["choice_c"],
                choice_d=item.get("choice_d", ""),
                correct_choice=item["correct_choice"].strip().upper(),
            )
            db.add(q)
            inserted += 1

    db.commit()
    db.close()
    print(f"Questions loaded: {inserted}, skipped: {skipped}")

if __name__ == "__main__":
    main()
