from rule_builder.rules import Rule

from ._helpers import has_castle_oblivion_rule, has_destiny_islands_rule, has_twilight_town_rule, has_world

WORLDS_UNLOCKED_BY_THEIR_CARD = (
    "Wonderland",
    "Olympus Coliseum",
    "Monstro",
    "Agrabah",
    "Halloween Town",
    "Atlantica",
    "Neverland",
    "Hollow Bastion",
    "100 Acre Wood",
)


def build_entrance_rules() -> dict[str, Rule]:
    entrance_rules: dict[str, Rule] = {}
    for world in WORLDS_UNLOCKED_BY_THEIR_CARD:
        entrance_rules[world] = has_world(world)
    entrance_rules["Twilight Town"] = has_twilight_town_rule()
    entrance_rules["Destiny Islands"] = has_destiny_islands_rule()
    entrance_rules["Castle Oblivion"] = has_castle_oblivion_rule()
    return entrance_rules


def build_rules() -> dict[str, Rule]:
    return {
        "100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)": has_world("Neverland") & has_world("Monstro"),
    }
