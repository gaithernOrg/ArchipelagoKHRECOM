from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from .Items import KHRECOMItem, get_items_by_group, item_name_groups, item_table
from .Locations import location_name_groups, location_table
from .Options import KHRECOMOptions, khrecom_option_groups
from .Presets import khrecom_option_presets
from .Regions import connect_entrances, create_regions
from .Rules import set_rules
from .GenerateSeedMod import CARD_VALUE_OPTION_NAMES, MAX_CARD_SETS, generate_seed_mod

POSSIBLE_STARTING_WORLDS = [
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
]
SHUFFLED_WORLD_IDS = [2, 3, 4, 5, 6, 7, 8, 9, 10]
POOL_GROUPS = ["World Unlocks", "Gold Map Cards", "Friend Cards", "Enemy Cards", "Sleights"]
FILLER_GROUP = "Sets"
LOCKED_FRIEND_CARD = "Friend Card Pluto"
LOCKED_FRIEND_CARD_LOCATION = "12F Exit Hall Larxene II (Enemy Cards Larxene)"
VICTORY_LOCATION = "Final Marluxia"


def launch_client():
    from .Client import launch
    launch_component(launch, name="KHRECOM Client")


components.append(Component("KHRECOM Client", "KHRECOMClient", func=launch_client, component_type=Type.CLIENT))


class KHRECOMWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Kingdom Hearts RE Chain of Memories Randomizer software on your computer. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "khrecom_en.md",
        "khrecom/en",
        ["Gicu"],
    )]
    option_groups = khrecom_option_groups
    options_presets = khrecom_option_presets


class KHRECOMWorld(World):
    """
    Kingdom Hearts RE Chain of Memories is an action card RPG following
    Sora on his journey through Castle Oblivion to find Riku and Kairi.
    """
    game = "Kingdom Hearts RE Chain of Memories"
    options_dataclass = KHRECOMOptions
    options: KHRECOMOptions
    topology_present = True
    web = KHRECOMWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.world_order = []

    def generate_early(self):
        self.decide_world_order()

    def create_regions(self):
        create_regions(self)

    def connect_entrances(self):
        connect_entrances(self)

    def create_items(self):
        self.place_predetermined_items()
        starting_worlds = self.give_starting_worlds()
        self.give_starting_cure()
        item_pool = self.build_item_pool(starting_worlds)
        self.fill_item_pool_with_filler(item_pool)
        self.multiworld.itempool += item_pool

    def set_rules(self):
        set_rules(self)

    def generate_output(self, output_directory: str):
        generate_seed_mod(self, output_directory)

    def create_item(self, name: str) -> KHRECOMItem:
        data = item_table[name]
        return KHRECOMItem(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        excluded_card_sets = ["Card Set " + card for card in self.options.exclude_cards.value]
        fillers = []
        for name in get_items_by_group(FILLER_GROUP):
            if self.is_excluded_card_set(name, excluded_card_sets):
                continue
            fillers.append(name)
        return self.random.choices(fillers, k=1)[0]

    def is_excluded_card_set(self, name: str, excluded_card_sets: List[str]) -> bool:
        for excluded_card_set in excluded_card_sets:
            if excluded_card_set in name:
                return True
        return False

    def decide_world_order(self) -> None:
        if len(self.world_order) > 0:
            return
        world_order = list(SHUFFLED_WORLD_IDS)
        self.random.shuffle(world_order)
        self.world_order = world_order

    def place_predetermined_items(self) -> None:
        self.get_location(LOCKED_FRIEND_CARD_LOCATION).place_locked_item(self.create_item(LOCKED_FRIEND_CARD))
        self.get_location(VICTORY_LOCATION).place_locked_item(self.create_item("Victory"))

    def give_starting_worlds(self) -> List[str]:
        if self.options.starting_worlds <= 0:
            return []
        world_count = min(self.options.starting_worlds.value, len(POSSIBLE_STARTING_WORLDS))
        starting_worlds = self.random.sample(POSSIBLE_STARTING_WORLDS, world_count)
        for starting_world in starting_worlds:
            self.multiworld.push_precollected(self.create_item(starting_world))
        return starting_worlds

    def give_starting_cure(self) -> None:
        if self.options.starting_cure:
            self.multiworld.push_precollected(self.create_item("Card Set Cure"))

    def build_item_pool(self, starting_worlds: List[str]) -> List[KHRECOMItem]:
        excluded_enemy_cards = ["Enemy Card " + card for card in self.options.exclude_enemy_cards.value]
        excluded_sleights = ["Sleight " + sleight for sleight in self.options.exclude_sleights.value]
        item_pool: List[KHRECOMItem] = []
        enemy_cards_added = 0
        sleights_added = 0
        shuffled_items = list(item_table.items())
        self.random.shuffle(shuffled_items)
        for name, data in shuffled_items:
            group = data.groups[0]
            if group not in POOL_GROUPS:
                continue
            if group == "Enemy Cards":
                if enemy_cards_added < self.options.enemy_card_amount and name not in excluded_enemy_cards:
                    enemy_cards_added = enemy_cards_added + 1
                    item_pool.append(self.create_item(name))
            elif group == "Sleights":
                if sleights_added < self.options.sleight_amount and name not in excluded_sleights:
                    sleights_added = sleights_added + 1
                    item_pool.append(self.create_item(name))
            elif name not in starting_worlds and name != LOCKED_FRIEND_CARD:
                item_pool.append(self.create_item(name))
        return item_pool

    def fill_item_pool_with_filler(self, item_pool: List[KHRECOMItem]) -> None:
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

    def get_card_set_data_string(self) -> str:
        lines = []
        for set_number in range(1, MAX_CARD_SETS + 1):
            card_values = []
            for card_value, option_name in enumerate(CARD_VALUE_OPTION_NAMES):
                if getattr(self.options, option_name).value == set_number:
                    card_values.append(str(card_value))
            lines.append(",".join(card_values) + "\n")
        return "".join(lines)

    def fill_slot_data(self) -> dict:
        world_order_string = ",".join(str(world_id) for world_id in self.world_order)
        return {
            "xpmult": int(self.options.exp_multiplier),
            "worldorder": world_order_string,
            "attackpower": int(self.options.attack_power),
            "setdata": self.get_card_set_data_string(),
        }
