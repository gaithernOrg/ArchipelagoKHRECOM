from rule_builder.rules import Has, HasAll, HasAny, HasFromListUnique, Rule

WORLD_CARDS = (
    "World Card Wonderland",
    "World Card Olympus Coliseum",
    "World Card Agrabah",
    "World Card Monstro",
    "World Card Atlantica",
    "World Card Halloween Town",
    "World Card Neverland",
    "World Card Hollow Bastion",
    "World Card 100 Acre Wood",
    "World Card Twilight Town",
    "World Card Destiny Islands",
)

FRIEND_CARDS = (
    "Friend Card Donald",
    "Friend Card Goofy",
    "Friend Card Aladdin",
    "Friend Card Ariel",
    "Friend Card Beast",
    "Friend Card Jack",
    "Friend Card Peter Pan",
    "Friend Card Pluto",
)

WORLDS_NEEDED_FOR_TWILIGHT_TOWN = 4
WORLDS_NEEDED_FOR_DESTINY_ISLANDS = 6
WORLDS_NEEDED_FOR_CASTLE_OBLIVION = 8


def has_world(world: str) -> Rule:
    return Has("World Card " + world)


def has_any_world(*worlds: str) -> Rule:
    return HasAny(*["World Card " + world for world in worlds])


def has_x_worlds_rule(number_of_worlds: int) -> Rule:
    return HasFromListUnique(*WORLD_CARDS, count=number_of_worlds)


def has_key_to_rewards(world: str) -> Rule:
    return Has("Key to Rewards " + world)


def has_twilight_town_rule() -> Rule:
    return has_world("Twilight Town") & has_x_worlds_rule(WORLDS_NEEDED_FOR_TWILIGHT_TOWN)


def has_destiny_islands_rule() -> Rule:
    return has_world("Destiny Islands") & has_x_worlds_rule(WORLDS_NEEDED_FOR_DESTINY_ISLANDS)


def has_castle_oblivion_rule() -> Rule:
    return HasAll(*FRIEND_CARDS) & has_x_worlds_rule(WORLDS_NEEDED_FOR_CASTLE_OBLIVION)
