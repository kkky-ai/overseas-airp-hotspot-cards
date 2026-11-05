#!/usr/bin/env python3
"""Build a portable ZIP containing the installable Skill directory."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skills" / "overseas-airp-hotspot-cards"
OUTPUT = ROOT / "dist" / "overseas-airp-hotspot-cards.zip"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and path.name != ".DS_Store" and "__pycache__" not in path.parts:
                archive.write(path, Path(SKILL.name) / path.relative_to(SKILL))
    print(OUTPUT)


if __name__ == "__main__":
    main()
