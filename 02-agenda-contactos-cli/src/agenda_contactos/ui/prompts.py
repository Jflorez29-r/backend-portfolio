def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid value. Enter an integer.")


def ask_text(prompt: str, allow_empty: bool = False) -> str | None:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if allow_empty:
            return None
        print("Value is required.")
