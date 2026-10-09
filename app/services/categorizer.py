import re

# Order matters: put specific phrases before generic words,
# so "peanut butter" hits pantry before "butter" hits dairy.
KEYWORDS: list[tuple[str, list[str]]] = [
    ("pantry",    ["peanut butter", "olive oil", "pasta", "rice", "flour"]),
    ("dairy",     ["milk", "cheese", "yogurt", "butter", "cream", "melk", "ost", "smør"]),
    ("meat",      ["chicken", "beef", "pork", "sausage", "kylling", "svin"]),
    ("fish",      ["salmon", "cod", "tuna", "laks", "torsk"]),
    ("fruit",     ["apple", "banana", "orange", "berry", "eple", "banan"]),
    ("vegetable", ["carrot", "broccoli", "spinach", "onion", "gulrot", "løk"]),
    ("bakery",    ["bread", "bun", "bagel", "brød"]),
]

DEFAULT_CATEGORY = "uncategorized"


def categorize(name: str) -> str:
    text = name.lower().strip()
    for category, words in KEYWORDS:
        for word in words:
            # \b anchors the match to the start of a word, so "ost" doesn't match "roast"
            if re.search(rf"\b{re.escape(word)}", text):
                return category
    return DEFAULT_CATEGORY


if __name__ == "__main__":
    # quick diagnostic: run `python -m app.services.categorizer`
    for sample in ["Organic whole milk", "Peanut butter", "Roast beef", "Gulrøtter", "Tofu"]:
        print(f"{sample!r:25} -> {categorize(sample)}")