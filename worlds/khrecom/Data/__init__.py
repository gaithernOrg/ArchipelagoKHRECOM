import csv
from importlib.resources import files
from typing import Dict, List


def load_rows(file_name: str) -> List[Dict[str, str]]:
    with files(__name__).joinpath(file_name).open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


items = load_rows("items.csv")
locations = load_rows("locations.csv")
