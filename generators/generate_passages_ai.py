import json
import random
import re
from pathlib import Path

from generators.ai_client import get_client

print(f"[generate_passages_ai] Running file: {Path(__file__).resolve()}")

THEMES = ["science", "sports", "play", "fiction", "life"]

THEME_GUIDE = {
    "science": "Simple science or nature",
    "sports": "Sports or physical activity",
    "play": "Kids play & hobbies",
    "fiction": "Light fiction",
    "life": "Everyday life",
}

# Adds "topic rotation" inside each theme so you don't get the same topics repeatedly.
# Requirement: at least 100 UNIQUE topics per theme.

TOPIC_BANK: dict[str, list[str]] = {
    "science": [
        "clouds and rain",
        "types of clouds",
        "the water cycle",
        "wind and breezes",
        "thunder and lightning (safe facts)",
        "fog and mist",
        "snowflakes",
        "hail and sleet (simple)",
        "rainbows and light",
        "shadows and light",
        "the sun as a star",
        "day and night",
        "seasons and tilt",
        "sunrise and sunset",
        "phases of the moon",
        "constellations",
        "planets in our solar system",
        "asteroids and comets",
        "gravity basics",
        "floating and sinking",
        "pushes and pulls",
        "friction on a slide",
        "magnets and paper clips",
        "static electricity (balloon trick)",
        "sound and vibrations",
        "pitch: high and low sounds",
        "echoes",
        "light reflecting in mirrors",
        "transparent vs opaque",
        "warm and cold",
        "melting and freezing",
        "evaporation (puddle disappears)",
        "condensation (cold glass)",
        "states of matter (solid/liquid/gas)",
        "mixing and dissolving (salt in water)",
        "filtering (sand and water)",
        "measuring with a thermometer",
        "measuring with a ruler",
        "simple machines: lever",
        "simple machines: pulley",
        "simple machines: wheel and axle",
        "simple machines: inclined plane",
        "simple machines: wedge",
        "simple machines: screw",
        "plant parts: roots",
        "plant parts: stem",
        "plant parts: leaves",
        "plant parts: flowers",
        "seeds and sprouting",
        "pollination by bees",
        "photosynthesis (kid level)",
        "plants need sunlight",
        "plants need water",
        "composting basics",
        "recycling and sorting",
        "reduce and reuse",
        "habitats: forest",
        "habitats: desert",
        "habitats: ocean",
        "habitats: pond",
        "habitats: grassland",
        "habitats: arctic",
        "animal camouflage",
        "animal migration",
        "animal hibernation",
        "nocturnal animals",
        "diurnal animals",
        "food chains",
        "herbivores, carnivores, omnivores",
        "adaptations: beaks",
        "adaptations: fur and feathers",
        "life cycle of a frog",
        "life cycle of a butterfly",
        "insects and habitats",
        "spiders vs insects",
        "worms and soil",
        "ants and teamwork",
        "bees and honey (facts)",
        "fish gills and breathing",
        "birds and wings",
        "mammals and babies",
        "reptiles and scales",
        "amphibians and wet skin",
        "the five senses",
        "taste and smell",
        "bones and muscles (basic)",
        "healthy sleep (basic science)",
        "germs and handwashing (simple)",
        "brushing teeth (why it helps)",
        "heart beats and exercise (kid safe)",
        "rocks vs minerals",
        "igneous rocks (simple)",
        "sedimentary rocks (simple)",
        "metamorphic rocks (simple)",
        "soil layers",
        "erosion by water",
        "erosion by wind",
        "volcanoes (safe facts)",
        "earthquakes (safe facts)",
        "maps and directions (simple)",
        "north, south, east, west",
        "using a compass (basic)",
        "tides (kid level)",
        "how boats float (simple)",
        "why ice floats",
        "why leaves change color",
        "why we see our breath (cold air)",
        "why bubbles are round",
        "why soap cleans",
    ],

    "sports": [
        "soccer passing",
        "soccer dribbling",
        "soccer shooting",
        "soccer goalkeeper basics",
        "soccer teamwork",
        "basketball dribbling",
        "basketball passing",
        "basketball shooting",
        "basketball defense (simple)",
        "baseball throwing",
        "baseball catching",
        "baseball batting (kid safe)",
        "softball basics",
        "tennis forehand",
        "tennis backhand",
        "tennis serving (simple)",
        "badminton rally",
        "table tennis quick reflexes",
        "volleyball bumping",
        "volleyball setting",
        "volleyball teamwork",
        "hockey skating basics",
        "hockey stopping safely",
        "hockey passing (simple)",
        "hockey teamwork",
        "ringette basics (simple)",
        "skating forward stride",
        "skating turning",
        "skating balance",
        "skating practice drills",
        "swimming lesson: kicking",
        "swimming lesson: floating",
        "swimming lesson: breathing",
        "swimming lesson: safety rules",
        "running a lap",
        "sprinting vs jogging (kid level)",
        "relay race baton pass",
        "warm-up and stretching",
        "cool-down breathing",
        "hydration during practice",
        "good sportsmanship",
        "sharing equipment",
        "listening to the coach",
        "setting a small goal",
        "practice and patience",
        "trying again after a miss",
        "team cheers",
        "learning new skills",
        "gymnastics balance beam (safe)",
        "gymnastics forward roll (safe)",
        "gymnastics flexibility",
        "martial arts class (safe, respectful)",
        "karate basics (safe)",
        "judo ukemi (safe falling basics)",
        "taekwondo kicks (safe basics)",
        "dance class rhythm",
        "dance class coordination",
        "yoga for kids",
        "jump rope singles",
        "jump rope double-unders (simple mention)",
        "hula hoop practice",
        "obstacle course at gym",
        "tag game teamwork",
        "capture-the-flag (safe rules)",
        "kickball game",
        "dodgeball alternatives (safe soft ball)",
        "frisbee throwing",
        "ultimate frisbee basics",
        "sledding rules (safe)",
        "skiing basics (kid safe)",
        "snowboarding balance (kid safe)",
        "tobogganing teamwork (kid safe)",
        "cycling with helmet safety",
        "scooter riding safety",
        "skateboard balance (kid safe)",
        "rollerblading safety gear",
        "rowing motion (simple)",
        "canoeing basics (kid safe)",
        "paddleboarding basics (kid safe)",
        "climbing wall rules (kid safe)",
        "bouldering basics (kid safe)",
        "archery range rules (kid safe, toy)",
        "bowling straight roll",
        "mini-golf putting",
        "golf swing basics (kid safe)",
        "track hurdles (low, kid safe)",
        "long jump practice",
        "high jump (kid safe intro)",
        "shot put with foam ball (kid safe)",
        "throwing accuracy game",
        "aiming at a target (soft beanbag)",
        "balance on one foot challenge",
        "reaction time game",
        "agility ladder drills",
        "cone weaving drills",
        "passing in pairs",
        "small-sided scrimmage",
        "referee signals (simple)",
        "keeping score fairly",
        "taking turns in drills",
        "encouraging a teammate",
        "being a good loser",
        "being a humble winner",
        "packing a sports bag",
        "tying skates or shoes",
        "wearing shin guards",
        "wearing a helmet",
        "practice at the rink",
        "practice at the pool",
        "practice in the gym",
        "practice on the field",
        "practice in the backyard",
    ],

    "play": [
        "building with blocks",
        "building a tall tower",
        "building a bridge with blocks",
        "making a marble run (safe)",
        "drawing a comic",
        "drawing animals",
        "drawing with crayons",
        "painting with watercolors",
        "making a collage",
        "paper cutting crafts (safe)",
        "origami easy shapes",
        "folding paper boats",
        "making paper airplanes",
        "testing paper airplane designs",
        "board game night",
        "card game matching",
        "puzzle challenge",
        "jigsaw puzzle teamwork",
        "word search game",
        "spot-the-difference game",
        "memory card game",
        "tic-tac-toe strategy",
        "checkers basics",
        "chess for kids (simple)",
        "domino chain fun",
        "LEGO sorting challenge",
        "toy car race track",
        "train set story",
        "dollhouse pretend play",
        "playing pretend store",
        "playing pretend restaurant",
        "playing pretend doctor (safe)",
        "playing pretend astronaut",
        "dress-up costumes",
        "puppet show",
        "making sock puppets",
        "shadow puppets (safe)",
        "music practice",
        "clapping rhythms",
        "learning a simple song",
        "playing recorder (school)",
        "playing piano basics",
        "drumming on a table (gentle)",
        "making a shaker instrument",
        "making a rubber-band guitar (safe)",
        "dance party at home",
        "freeze dance game",
        "musical chairs (safe rules)",
        "sing-along time",
        "story time with a parent",
        "reading with a buddy",
        "library scavenger hunt (safe)",
        "writing a short poem",
        "writing a silly riddle",
        "making up tongue twisters",
        "creating a secret code (simple)",
        "stamp collecting (kid version)",
        "sticker sorting",
        "coloring contest",
        "making a poster",
        "making a birthday card",
        "thank-you card craft",
        "paper chain decorations",
        "making snowflakes from paper",
        "making a bookmark",
        "making a mini book",
        "building a fort with blankets",
        "pretend camping in a fort",
        "flashlight shadow game (safe)",
        "treasure hunt indoors (safe)",
        "scavenger hunt at home",
        "sorting buttons by color",
        "sorting toys by size",
        "counting game with snacks (safe)",
        "measuring with string",
        "building with cardboard boxes",
        "making a robot costume (box)",
        "recycling craft project",
        "clay modeling (non-toxic)",
        "playdough shapes",
        "making a pretend map",
        "creating a city on paper",
        "drawing a maze",
        "solving a maze",
        "making a friendship bracelet",
        "bead pattern making (safe)",
        "weaving with paper strips",
        "simple sewing with felt (safe)",
        "button art",
        "magnet tiles building",
        "building a spaceship model",
        "building a zoo model",
        "building a school model",
        "making a puppet theater",
        "role-play: teacher and student",
        "role-play: news reporter",
        "role-play: detective (safe)",
        "role-play: chef",
        "kitchen pretend baking",
        "toy kitchen cooking",
        "garden pretend store",
        "chalk drawing on sidewalk",
        "hopscotch game",
        "jumping games with friends",
        "swing set play (safe)",
        "slide game (safe)",
        "sandbox building",
        "building sand castles",
        "bubble blowing contest",
        "bubble wand making (safe)",
        "kite flying (kid safe)",
        "paper fan craft",
        "making a mini flag",
        "crafting with pom-poms",
        "crafting with pipe cleaners",
        "making a simple mask (paper)",
        "making a crown",
    ],

    "fiction": [
        "a friendly talking squirrel",
        "a talking cat who loves books",
        "a dog who solves small mysteries (safe)",
        "a rabbit with a tiny backpack",
        "a penguin who learns to dance",
        "a turtle who loves races (slow and steady)",
        "a fox who collects buttons (kind fox)",
        "a bear who bakes muffins (safe)",
        "a mouse with a big idea",
        "a dolphin who finds a shiny shell (safe)",
        "a tiny dragon who loves tea",
        "a tiny dragon who hates loud noise (gentle)",
        "a gentle unicorn in a garden",
        "a shy unicorn at a festival (safe)",
        "a robot learning feelings",
        "a robot that makes paper hats",
        "a robot that learns jokes",
        "a wind-up toy that walks away (safe)",
        "a toy train that whispers stories",
        "a library book with riddles",
        "a book that changes pictures (magic, safe)",
        "a pencil that draws real stickers (safe)",
        "a crayon that changes colors",
        "a kind magic button (safe)",
        "a magic button that plays music",
        "a magic scarf that stays warm (safe)",
        "a magic umbrella that makes shade",
        "a mailbox that sings",
        "a doorbell that tells puns",
        "a clock that tells silly time (safe)",
        "a talking backpack at school",
        "a talking lunchbox",
        "a talking skateboard (safe)",
        "a friendly ghost that hates scary stories (gentle)",
        "a cloud that follows a kid",
        "a cloud that makes shapes",
        "a raindrop who wants to be a snowflake",
        "a snowflake who visits a mitten",
        "a leaf that rides the wind",
        "a pebble that wants to skip",
        "a star that falls into a pocket (safe)",
        "a moonbeam in a jar (safe)",
        "a tiny spaceship in a lunchbox (safe)",
        "a friendly alien at the playground",
        "a friendly alien learns recess rules",
        "a rainbow that loses a color",
        "a rainbow that paints a fence (safe)",
        "a garden gnome who loves math",
        "a garden gnome who writes notes",
        "a brave little spoon",
        "a brave little sock",
        "a shy hat who wants a friend",
        "a brave mitten in winter",
        "a button that rolls away",
        "a balloon that won’t pop (safe)",
        "a bubble that can talk (safe)",
        "a paper boat on a tiny adventure",
        "a paper airplane that delivers a note",
        "a kite that finds a new friend",
        "a scarf that tells riddles",
        "a mirror that shows silly outfits (safe)",
        "a lamp that makes cozy light",
        "a chair that squeaks songs",
        "a teacup that tells stories",
        "a cookie that doesn’t want to be eaten (funny)",
        "a carrot who wants to skateboard (silly)",
        "a broccoli who wants to sing (silly)",
        "a pancake that flips itself (silly)",
        "a waffle who starts a club (silly)",
        "a friendly monster who loves naps (not scary)",
        "a friendly monster who collects leaves",
        "a tiny fairy who can’t find her shoes (safe)",
        "a fairy who makes tiny signs (safe)",
        "a wizard who only knows helpful spells (safe)",
        "a wizard who turns soup into stew (safe)",
        "a spell that makes everyone giggle (safe)",
        "a classroom chalk that draws smiley faces",
        "a school bell that says hello",
        "a hallway that becomes a maze (safe, short)",
        "a lunchroom table with secrets (silly)",
        "a playground slide that tells jokes",
        "a swing that wants to fly (safe)",
        "a seesaw that balances emotions (gentle)",
        "a scooter that hums music",
        "a bicycle that loves slow rides (safe)",
        "a mystery of the missing sticker (safe)",
        "a mystery of the missing bookmark (safe)",
        "a mystery of the lost mitten (safe)",
        "a treasure hunt for a silly prize (safe)",
        "a secret clubhouse under the stairs (safe)",
        "a friendly crow who returns lost things",
        "a raccoon who loves recycling (funny)",
        "a squirrel who runs a tiny shop (funny)",
        "a penguin who opens a lemonade stand (silly)",
        "a llama who learns to whisper (silly)",
        "a hedgehog who hosts a tea party (safe)",
        "a snail who wins a ribbon (safe)",
        "a fish who learns to blow bubbles (safe)",
        "a frog who starts a band (safe)",
        "a butterfly who writes postcards (safe)",
        "a bee who learns to count flowers (safe)",
        "a ladybug who wants a cape (silly)",
        "a spider who knits a scarf (gentle)",
        "a worm who wants a library card (silly)",
        "a dolphin who learns a new game (safe)",
        "a whale who sings soft songs (safe)",
    ],

    "life": [
        "packing a lunch",
        "choosing a healthy snack",
        "helping with groceries",
        "carrying a small bag (safe)",
        "setting the table",
        "clearing the table",
        "washing dishes (kid safe)",
        "sorting laundry colors",
        "folding towels",
        "making the bed",
        "feeding a pet (safe)",
        "refilling a water bowl",
        "brushing teeth routine",
        "getting ready for school",
        "finding a missing shoe",
        "tying shoelaces",
        "zipping a coat",
        "waiting for the bus",
        "bus manners (quiet voices)",
        "crossing the street safely",
        "walking to school with a parent",
        "first day at a new class",
        "meeting a new friend",
        "being a good friend",
        "sharing supplies",
        "taking turns",
        "learning to apologize",
        "accepting an apology",
        "using kind words",
        "including someone in a game",
        "handling big feelings (simple)",
        "calming down with breaths",
        "asking for help",
        "helping a classmate",
        "reading in the library",
        "getting a library card",
        "returning a book on time",
        "classroom jobs",
        "line leader job",
        "lunchroom etiquette",
        "recess rules",
        "playing fairly at recess",
        "rainy day indoor recess",
        "show and tell day",
        "bringing a special item (safe)",
        "making a thank-you note",
        "writing a birthday card",
        "calling a grandparent",
        "family movie night",
        "family game night",
        "a family tradition",
        "helping cook dinner (kid safe)",
        "washing fruits (kid safe)",
        "making a simple sandwich (kid safe)",
        "helping bake cookies (kid safe)",
        "going to the grocery store",
        "choosing fruit at the market",
        "using a shopping list",
        "counting coins (simple)",
        "saving money in a jar",
        "choosing between two toys",
        "doing a small chore",
        "watering plants",
        "raking leaves (kid safe)",
        "shoveling a tiny path (kid safe)",
        "cleaning up toys",
        "organizing a desk",
        "packing a backpack",
        "checking homework folder",
        "finishing homework early",
        "practice reading aloud",
        "practice spelling words",
        "music lesson day",
        "sports practice day",
        "wearing a helmet",
        "getting fitted for skates",
        "learning rink rules",
        "going to the pool",
        "pool safety rules",
        "doctor checkup (not scary)",
        "dentist visit (not scary)",
        "getting a haircut",
        "trying a new food",
        "helping a neighbor",
        "borrowing and returning items",
        "finding a lost item (safe)",
        "re-tracing steps (simple)",
        "being on time",
        "waiting patiently",
        "sharing attention (taking turns speaking)",
        "listening to directions",
        "following a schedule",
        "planning a playdate",
        "inviting someone to play",
        "saying no politely",
        "making a compromise",
        "solving a small disagreement",
        "using “I feel” statements (simple)",
        "helping set up a party",
        "cleaning after a party",
        "packing for a short trip",
        "helping with recycling",
        "sorting trash vs recycling",
        "donating old toys (gentle)",
        "writing a simple journal entry",
        "drawing feelings",
        "choosing a bedtime story",
        "bedtime routine",
    ],
}

STRUCTURE_TEMPLATES = [
    "narrative",
    "dialogue",
    "fact_card",
    "steps",
    "compare_contrast",
    "cause_effect",
]

OUT_DIR = Path("data/passages")
OUT_DIR.mkdir(parents=True, exist_ok=True)

GRADES = {
    1: {"min_words": 30, "max_words": 60},
    2: {"min_words": 60, "max_words": 90},
    3: {"min_words": 90, "max_words": 130},
    4: {"min_words": 130, "max_words": 170},
    5: {"min_words": 170, "max_words": 220},
}

PASSAGES_PER_GRADE = 100
MAX_ATTEMPTS = 15

SYSTEM = "You generate reading passages for children. Return only valid JSON."

def word_count(t: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", t))

def trim_to_max_words(text: str, max_words: int) -> str:
    words = re.findall(r"[A-Za-z0-9']+|[^\sA-Za-z0-9']+", text)
    out, wc = [], 0
    for tok in words:
        if re.match(r"[A-Za-z0-9']+$", tok):
            if wc + 1 > max_words:
                break
            wc += 1
        out.append(tok)
    t = "".join(out).strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t

def normalize_punctuation(s: str) -> str:
    # Convert curly quotes/dashes to plain ASCII so they don't appear as \u2019 etc.
    return (
        s.replace("\u2019", "'")
         .replace("\u2018", "'")
         .replace("\u201c", '"')
         .replace("\u201d", '"')
         .replace("\u2013", "-")
         .replace("\u2014", "-")
         .replace("\u00a0", " ")
    )

def normalize_whitespace(text: str) -> str:
    # Replace newline blocks with a single space, then collapse spaces
    text = re.sub(r"\s*\n+\s*", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

def passage_prompt(g: int, c: str, th: str, tp: str, st: str, spec: dict) -> str:
    return f"""
Write ONE reading passage for Grade {g}.
Theme: {th}
Topic: {tp}
Structure: {st}

Word count: {spec['min_words']}–{spec['max_words']}

Return JSON only:
{{"grade":{g},"passage_code":"{c}","title":"...","text":"..."}}
""".strip()

def generate_one(client, grade: int, code: str, theme: str, topic: str, structure: str, spec: dict) -> dict:
    model = "gpt-4.1" if grade == 1 else "gpt-4.1-mini"

    for _ in range(MAX_ATTEMPTS):
        r = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": passage_prompt(grade, code, theme, topic, structure, spec)},
            ],
            temperature=0.8,
        )

        raw = r.choices[0].message.content.strip()

        try:
            data = json.loads(raw)
        except Exception:
            continue

        # Enforce invariants
        data["grade"] = grade
        data["passage_code"] = code

        # Basic shape checks
        if not isinstance(data.get("title"), str) or not isinstance(data.get("text"), str):
            continue
        if not data["title"].strip() or not data["text"].strip():
            continue

        # Normalize punctuation + whitespace (removes \u2019 and \n\n issues)
        data["title"] = normalize_punctuation(data["title"])
        data["text"] = normalize_punctuation(data["text"])
        data["text"] = normalize_whitespace(data["text"])

        # Trim if too long
        if word_count(data["text"]) > spec["max_words"]:
            data["text"] = trim_to_max_words(data["text"], spec["max_words"])
            data["text"] = normalize_whitespace(data["text"])

        # Normalize again after trimming
        data["title"] = normalize_punctuation(data["title"])
        data["text"] = normalize_punctuation(data["text"])
        data["text"] = normalize_whitespace(data["text"])

        wc = word_count(data["text"])
        if spec["min_words"] <= wc <= spec["max_words"]:
            return data

    raise RuntimeError(f"Failed generation for {code}")

def main():
    client = get_client()

    for grade in range(1, 6):
        print(f"Grade {grade}: generating {PASSAGES_PER_GRADE}")
        items = []

        for i in range(1, PASSAGES_PER_GRADE + 1):
            code = f"G{grade}-{i:03d}"
            tries = 0
            last_err = None

            while tries < 4:
                tries += 1
                theme = random.choice(THEMES)

                if not TOPIC_BANK.get(theme):
                    raise ValueError(f"TOPIC_BANK['{theme}'] is empty. Paste topics before running.")

                topic = random.choice(TOPIC_BANK[theme])

                # fallback: for Grade 1, avoid “steps” as a first choice
                if grade == 1 and tries >= 2:
                    structure = "narrative"
                else:
                    structure = random.choice(STRUCTURE_TEMPLATES)

                print(f"Generating {code} ({theme}, {topic}, {structure}) [try {tries}]")

                try:
                    items.append(generate_one(client, grade, code, theme, topic, structure, GRADES[grade]))
                    break
                except Exception as e:
                    last_err = e

            if tries >= 4 and last_err:
                print(f"SKIP {code}: {last_err}")
                continue

            # Write safely (ensure_ascii=False keeps unicode readable)
            out_path = OUT_DIR / f"grade{grade}.json"
            out_path.write_text(
                json.dumps(items, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

        print(f"Grade {grade} complete.")

if __name__ == "__main__":
    main()
