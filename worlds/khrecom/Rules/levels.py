from rule_builder.rules import Rule

from ._helpers import has_x_worlds_rule

WORLDS_NEEDED = {
    "Level 12 (Sleight Strike Raid)": 2,
    "Level 17 (Sleight Blitz)": 2,
    "Level 22 (Sleight Zantetsuken)": 3,
    "Level 27 (Sleight Sonic Blade)": 3,
    "Level 32 (Sleight Lethal Frame)": 4,
    "Level 37 (Sleight Tornado)": 4,
    "Level 42 (Sleight Ars Arcanum)": 5,
    "Level 47 (Sleight Holy)": 5,
    "Level 52 (Sleight Ragnarok)": 6,
    "Level 57 (Sleight Mega Flare)": 6,
}


def build_rules(khrecomworld) -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    if not khrecomworld.options.levels:
        return location_rules
    for location_name, number_of_worlds in WORLDS_NEEDED.items():
        location_rules[location_name] = has_x_worlds_rule(number_of_worlds)
    return location_rules
