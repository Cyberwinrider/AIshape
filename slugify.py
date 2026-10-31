"""Convert an ASCII English title into a URL-friendly slug.

Example:
    >>> slugify("Hello, World!")
    'hello-world'
"""

import re

_NON_SLUG_CHARS = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return a lowercase hyphen-separated slug for *text*.

    Every maximal run of characters that is not an ASCII lowercase letter
    (a-z) or an ASCII digit (0-9) is replaced by a single "-", then leading
    and trailing hyphens are stripped. An empty string, or one containing
    only non-alphanumeric characters, yields "".
    """
    slug = _NON_SLUG_CHARS.sub("-", text.lower())
    return slug.strip("-")
