from rule_builder.rules import Rule

from ..Locations import location_table
from ._helpers import has_key_to_rewards

ROOM_OF_REWARDS = " Room of Rewards"


def build_rules() -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    for location_name in location_table:
        if ROOM_OF_REWARDS not in location_name:
            continue
        world = location_name.split(ROOM_OF_REWARDS)[0]
        location_rules[location_name] = has_key_to_rewards(world)
    return location_rules
