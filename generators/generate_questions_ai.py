import json
import random
from pathlib import Path
from typing import Any, List, Tuple

from generators.ai_client import get_client

PASSAGES_DIR = Path("data/passages")
QUESTIONS_DIR = Path("data/questions")
QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)

QUESTIONS_PER_GRADE = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5}

SYSTEM = (
    "You write multiple-choice reading comprehension questions for children. "
    "Return only valid JSON. No markdown. No commentary."
)

def questions_prompt(grade: int, passage_code: str, title: str, text: str, n: int) -> str:
    return f"""
Create {n} multiple-choice questions for this Grade {grade} passage.

Passage code: {passage_code}
Title: {title}
Text: {text}

Requirements:
- Each question must have 4 choices (A,B,C,D)
- Exactly one correct choice
- Correct choice must be obvious from the text (Grades 1-2 mostly literal)
- Grade 3+: include at most one simple inference question
- Avoid tricky wording

Return JSON array of objects with EXACT keys:
[
  {{
    "passage_code": "{passage_code}",
    "prompt": "...",
    "choice_a": "...",
    "choice_b": "...",
    "choice_c": "...",
    "choice_d": "...",
    "correct_choice": "A"
  }}
]

Rules:
- correct_choice must be one of: A, B, C, D
- keep prompts short
""".strip()

def _normalize_text(s: str) -> str:
    return (s or "").strip()

def _shuffle_choices(correct_letter: str, choices: List[str]) -> Tuple[List[str], str]:
    """
    Input:
      - correct_letter: "A"/"B"/"C"/"D" indicating which original choice is correct
      - choices: [choice_a, choice_b, choice_c, choice_d]
    Output:
      - shuffled choices list (length 4)
      - new correct letter after shuffling
    """
    letters = ["A", "B", "C", "D"]
    correct_idx = letters.index(correct_letter)

    # Pair each choice with its original letter so we can track the correct one
    pairs = [(letters[i], _normalize_text(choices[i])) for i in range(4)]

    # Basic guard: ensure all choices are non-empty after normalization
    if any(not text for _, text in pairs):
        return [p[1] for p in pairs], correct_letter

    random.shuffle(pairs)

    # Find where the originally-correct choice ended up
    correct_text = _normalize_text(choices[correct_idx])
    new_correct_idx = next(i for i, (_, t) in enumerate(pairs) if _normalize_text(t) == correct_text)
    new_correct_letter = letters[new_correct_idx]

    return [t for _, t in pairs], new_correct_letter

def generate_questions(client, grade: int, passage: dict[str, Any]) -> list[dict[str, Any]]:
    n = QUESTIONS_PER_GRADE[grade]
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": questions_prompt(
                    grade,
                    passage["passage_code"],
                    passage["title"],
                    passage["text"],
                    n,
                ),
            },
        ],
        temperature=0.4,
    )
    content = resp.choices[0].message.content.strip()
    data = json.loads(content)

    for q in data:
        # basic checks
        assert q["passage_code"] == passage["passage_code"]
        assert q["correct_choice"] in ["A", "B", "C", "D"]
        for k in ["prompt", "choice_a", "choice_b", "choice_c", "choice_d"]:
            assert isinstance(q[k], str) and len(q[k].strip()) > 0

        # NEW: shuffle choices and update correct_choice accordingly
        original_choices = [q["choice_a"], q["choice_b"], q["choice_c"], q["choice_d"]]
        shuffled, new_correct = _shuffle_choices(q["correct_choice"], original_choices)

        q["choice_a"], q["choice_b"], q["choice_c"], q["choice_d"] = shuffled
        q["correct_choice"] = new_correct

    return data

def main():
    client = get_client()

    for grade in range(1, 6):
        passage_file = PASSAGES_DIR / f"grade{grade}.json"
        passages = json.loads(passage_file.read_text(encoding="utf-8"))

        out_questions: list[dict[str, Any]] = []
        for p in passages:
            print(f"Generating questions for {p['passage_code']}...")
            out_questions.extend(generate_questions(client, grade, p))

        out_path = QUESTIONS_DIR / f"grade{grade}_questions.json"
        out_path.write_text(json.dumps(out_questions, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
