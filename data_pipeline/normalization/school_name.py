import unicodedata


def normalize_school_name(name: str) -> str:

    if not isinstance(name, str):
        raise TypeError("School name must be a string")

    name = unicodedata.normalize("NFKC", name)

    name = name.casefold()

    name = "".join(" " if unicodedata.category(char).startswith("P") else char for char in name)

    name = " ".join(name.split())

    if not name:
        raise ValueError("School name cannot be empty")

    return name
