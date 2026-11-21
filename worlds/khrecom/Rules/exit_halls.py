from rule_builder.rules import Rule

from ._helpers import has_x_worlds_rule

WORLDS_NEEDED = {
    "06F Exit Hall Larxene I (Magic Cards Thunder)": 4,
    "06F Exit Hall Larxene I (Sleight Thundara)": 4,
    "06F Exit Hall Larxene I (Sleight Thundaga)": 4,
    "07F Exit Hall Riku I (Magic Cards Aero)": 5,
    "07F Exit Hall Riku I (Sleight Aerora)": 5,
    "07F Exit Hall Riku I (Sleight Aeroga)": 5,
    "08F Exit Hall Riku II (Sleight Magnet Spiral)": 5,
    "10F Exit Hall Vexen I (Sleight Freeze)": 6,
    "11F Exit Hall Riku III (Item Cards Mega-Potion)": 6,
    "12F Exit Hall Larxene II (Attack Cards Oblivion)": 7,
    "12F Exit Hall Larxene II (Enemy Cards Larxene)": 7,
    "12F Exit Hall Riku IV (Enemy Cards Riku)": 7,
}


def build_rules() -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    for location_name, number_of_worlds in WORLDS_NEEDED.items():
        location_rules[location_name] = has_x_worlds_rule(number_of_worlds)
    return location_rules
