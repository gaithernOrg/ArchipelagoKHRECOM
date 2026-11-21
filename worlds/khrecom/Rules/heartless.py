from typing import NamedTuple, Tuple

from rule_builder.rules import Or, Rule

from ._helpers import has_any_world, has_castle_oblivion_rule, has_destiny_islands_rule, has_twilight_town_rule

DEFEAT_COUNTS = (1, 2, 3)


class HeartlessHabitat(NamedTuple):
    worlds: Tuple[str, ...] = ()
    twilight_town: bool = False
    destiny_islands: bool = False
    castle_oblivion: bool = False


HABITATS = {
    "Air Pirate":     HeartlessHabitat(worlds=("Neverland",)),
    "Pirate":         HeartlessHabitat(worlds=("Neverland",)),
    "Air Soldier":    HeartlessHabitat(worlds=("Monstro", "Agrabah"), twilight_town=True),
    "Aquatank":       HeartlessHabitat(worlds=("Atlantica",)),
    "Screwdiver":     HeartlessHabitat(worlds=("Atlantica",)),
    "Sea Neon":       HeartlessHabitat(worlds=("Atlantica",)),
    "Bandit":         HeartlessHabitat(worlds=("Agrabah",)),
    "Fat Bandit":     HeartlessHabitat(worlds=("Agrabah",)),
    "Barrel Spider":  HeartlessHabitat(worlds=("Monstro", "Agrabah", "Neverland")),
    "Bouncywild":     HeartlessHabitat(worlds=("Olympus Coliseum",)),
    "Powerwild":      HeartlessHabitat(worlds=("Olympus Coliseum",)),
    "Creeper Plant":  HeartlessHabitat(worlds=("Wonderland", "Halloween Town"), destiny_islands=True),
    "Crescendo":      HeartlessHabitat(worlds=("Wonderland", "Neverland"), destiny_islands=True),
    "Darkball":       HeartlessHabitat(worlds=("Atlantica", "Neverland"), destiny_islands=True, castle_oblivion=True),
    "Defender":       HeartlessHabitat(worlds=("Hollow Bastion",), castle_oblivion=True),
    "Gargoyle":       HeartlessHabitat(worlds=("Halloween Town",)),
    "Wight Knight":   HeartlessHabitat(worlds=("Halloween Town",)),
    "Green Requiem":  HeartlessHabitat(worlds=("Monstro", "Agrabah"), castle_oblivion=True),
    "Large Body":     HeartlessHabitat(worlds=("Wonderland", "Olympus Coliseum", "Monstro")),
    "Neoshadow":      HeartlessHabitat(castle_oblivion=True),
    "Search Ghost":   HeartlessHabitat(worlds=("Monstro", "Atlantica", "Halloween Town")),
    "Tornado Step":   HeartlessHabitat(worlds=("Monstro", "Hollow Bastion"), destiny_islands=True),
    "Wizard":         HeartlessHabitat(worlds=("Hollow Bastion",), castle_oblivion=True),
    "Wyvern":         HeartlessHabitat(worlds=("Hollow Bastion",), castle_oblivion=True),
    "Yellow Opera":   HeartlessHabitat(worlds=("Monstro", "Agrabah", "Neverland"), castle_oblivion=True),
}


def build_habitat_rule(habitat: HeartlessHabitat) -> Rule:
    ways_to_find: list[Rule] = []
    if habitat.worlds:
        ways_to_find.append(has_any_world(*habitat.worlds))
    if habitat.twilight_town:
        ways_to_find.append(has_twilight_town_rule())
    if habitat.destiny_islands:
        ways_to_find.append(has_destiny_islands_rule())
    if habitat.castle_oblivion:
        ways_to_find.append(has_castle_oblivion_rule())
    if len(ways_to_find) == 1:
        return ways_to_find[0]
    return Or(*ways_to_find)


def build_rules() -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    for heartless, habitat in HABITATS.items():
        rule = build_habitat_rule(habitat)
        for defeat_count in DEFEAT_COUNTS:
            location_rules[f"Defeat {defeat_count} Heartless {heartless}"] = rule
    return location_rules
