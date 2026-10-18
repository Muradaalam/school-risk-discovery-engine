import unicodedata


ABBREVIATIONS = {
    "govt": "government",
}


def normalize_school_name(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("School name must be a string")

    name = unicodedata.normalize("NFKC", name)
    name = name.casefold()

    name = "".join(" " if unicodedata.category(char).startswith("P") else char for char in name)

    words = name.split()
    words = [ABBREVIATIONS.get(word, word) for word in words]

    name = " ".join(words)

    if not name:
        raise ValueError("School name cannot be empty")

    return name