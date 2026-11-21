from typing import Dict, List, NamedTuple, Set, Tuple

from BaseClasses import Location
from . import Data


class KHRECOMLocation(Location):
    game: str = "Kingdom Hearts RE Chain of Memories"


class KHRECOMLocationData(NamedTuple):
    region: str
    code: int
    groups: Tuple[str, ...] = ()
    option: str = ""


def get_locations_by_group(group: str) -> Dict[str, KHRECOMLocationData]:
    return {name: data for name, data in location_table.items() if group in data.groups}


def build_location_table(rows: List[Dict[str, str]]) -> Dict[str, KHRECOMLocationData]:
    table: Dict[str, KHRECOMLocationData] = {}
    for row in rows:
        table[row["name"]] = KHRECOMLocationData(
            row["region"],
            code=int(row["id"]),
            groups=tuple(row["groups"].split(";")) if row["groups"] else (),
            option=row["option"],
        )
    return table


def build_location_name_groups(table: Dict[str, KHRECOMLocationData]) -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}
    for name, location in table.items():
        for group in location.groups:
            groups.setdefault(group, set()).add(name)
    return groups


location_table: Dict[str, KHRECOMLocationData] = build_location_table(Data.locations)
location_name_groups: Dict[str, Set[str]] = build_location_name_groups(location_table)
lookup_id_to_name: Dict[int, str] = {data.code: name for name, data in location_table.items()}
