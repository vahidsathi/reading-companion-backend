from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.passage import Passage

def main():
    db = SessionLocal()

    for grade in range(1, 6):
        passages = db.execute(
            select(Passage)
            .where(Passage.grade == grade)
            .order_by(Passage.id)
        ).scalars().all()

        counter = 1
        for p in passages:
            if p.passage_code:
                continue  # don't overwrite existing codes

            p.passage_code = f"G{grade}-{counter:03d}"
            counter += 1

    db.commit()
    db.close()
    print("Passage codes assigned.")

if __name__ == "__main__":
    main()
