def normalize_udise_code(code: str) -> str:
    if not isinstance(code, str):
        raise TypeError("UDISE code must be a string")

    code = code.strip()

    if len(code) != 11:
        raise ValueError("UDISE code must contain exactly 11 digits")

    if not code.isascii() or not code.isdigit():
        raise ValueError("UDISE code must contain only digits")

    return code


def match_udise_codes(first: str | None, second: str | None) -> bool:
    if first is None or second is None:
        return False

    return normalize_udise_code(first) == normalize_udise_code(second)