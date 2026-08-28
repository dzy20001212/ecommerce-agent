import re
from dataclasses import dataclass


@dataclass
class MaskResult:
    text: str
    masked_count: int


PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(1[3-9]\d)"
    r"\d{4}"
    r"(\d{4})"
    r"(?!\d)"
)


EMAIL_PATTERN = re.compile(
    r"\b"
    r"([A-Za-z0-9._%+-]{1,3})"
    r"[A-Za-z0-9._%+-]*"
    r"@"
    r"([A-Za-z0-9.-]+\.[A-Za-z]{2,})"
    r"\b"
)


def mask_sensitive_data(
    text: str
) -> MaskResult:

    masked_count = 0


    def mask_phone(match):

        nonlocal masked_count

        masked_count += 1

        return (
            f"{match.group(1)}"
            f"****"
            f"{match.group(2)}"
        )


    def mask_email(match):

        nonlocal masked_count

        masked_count += 1

        return (
            f"{match.group(1)}"
            f"***@"
            f"{match.group(2)}"
        )


    result = PHONE_PATTERN.sub(
        mask_phone,
        text
    )


    result = EMAIL_PATTERN.sub(
        mask_email,
        result
    )


    return MaskResult(
        text=result,
        masked_count=masked_count,
    )