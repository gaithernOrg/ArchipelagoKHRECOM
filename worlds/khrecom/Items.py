from typing import Dict, List, NamedTuple, Set, Tuple

from BaseClasses import Item, ItemClassification
from . import Data


class KHRECOMItem(Item):
    game: str = "Kingdom Hearts RE Chain of Memories"


class KHRECOMItemData(NamedTuple):
    groups: Tuple[str, ...]
    code: int
    classification: ItemClassification = ItemClassification.filler


def get_items_by_group(group: str) -> Dict[str, KHRECOMItemData]:
    return {name: data for name, data in item_table.items() if group in data.groups}


def build_item_table(rows: List[Dict[str, str]]) -> Dict[str, KHRECOMItemData]:
    table: Dict[str, KHRECOMItemData] = {}
    for row in rows:
        table[row["name"]] = KHRECOMItemData(
            tuple(row["groups"].split(";")),
            code=int(row["id"]),
            classification=ItemClassification[row["classification"]],
        )
    return table


def build_item_name_groups(table: Dict[str, KHRECOMItemData]) -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {}
    for name, item in table.items():
        for group in item.groups:
            groups.setdefault(group, set()).add(name)
    return groups


item_table: Dict[str, KHRECOMItemData] = build_item_table(Data.items)
item_name_groups: Dict[str, Set[str]] = build_item_name_groups(item_table)
