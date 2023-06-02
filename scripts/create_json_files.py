import os
import re
from pathlib import Path
from typing import IO, Any, Iterable


def get_files() -> Iterable[str]:
    """"""
    for root, _, files in os.walk("./"):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def main():
    json_path = Path("./dicts/")
    if not json_path.exists():
        json_path.mkdir()

    files = get_files()
    for file in files:
        with open(file, encoding="utf-8") as f:
            results: list[str] = re.findall(r'open\("./dicts/(.*?.json)"', f.read())
            for r in results:
                json_file = json_path / r
                if not json_file.exists():
                    json_file.touch()
                    if r == "Colour.json":
                        json_file.write_text('{"colour": "000000"}')
                    else:
                        json_file.write_text("{}")
                    print(f"Created {json_file}")


if __name__ == "__main__":
    main()
