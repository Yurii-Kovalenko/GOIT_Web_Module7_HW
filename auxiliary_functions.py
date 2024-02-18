from sqlalchemy.orm import declarative_base

Base = declarative_base()


def input_in_range(text: str, begin: int, end: int) -> int:
    while True:
        number = input(f"{text}({begin}...{end}): ")
        if number.isdigit():
            result = int(number)
            if begin - 1 < result < end + 1:
                break
    return result
