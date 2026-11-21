import json
import os
import zipfile
from typing import Dict, List, Optional

import Utils
from worlds.Files import APPlayerContainer

FLOOR_COUNT = 13
FIRST_SHUFFLED_WORLD = 2
MAX_CARD_SETS = 20
CARD_VALUE_OPTION_NAMES = [
    "value_0_on", "value_1_on", "value_2_on", "value_3_on", "value_4_on",
    "value_5_on", "value_6_on", "value_7_on", "value_8_on", "value_9_on",
    "value_0_p_on", "value_1_p_on", "value_2_p_on", "value_3_p_on", "value_4_p_on",
    "value_5_p_on", "value_6_p_on", "value_7_p_on", "value_8_p_on", "value_9_p_on",
]


class KHRECOMSeedMod(APPlayerContainer):
    game: str = "Kingdom Hearts RE Chain of Memories"
    patch_file_ending = ".zip"

    def __init__(self, files: Dict[str, str], path: str, player: Optional[int] = None,
                 player_name: str = "", server: str = ""):
        self.files = files
        super().__init__(path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for file_name, text in self.files.items():
            opened_zipfile.writestr(file_name, text)
        super().write_contents(opened_zipfile)


def get_floor_worlds(world_order: List[int]) -> List[int]:
    floor_worlds = list(range(1, FLOOR_COUNT + 1))
    for position, floor_number in enumerate(world_order):
        world_id = position + FIRST_SHUFFLED_WORLD
        floor_worlds[floor_number - 1] = world_id
    return floor_worlds


def get_card_sets(options) -> List[List[int]]:
    all_sets = []
    for set_number in range(1, MAX_CARD_SETS + 1):
        card_values = []
        for card_value, option_name in enumerate(CARD_VALUE_OPTION_NAMES):
            if getattr(options, option_name).value == set_number:
                card_values.append(card_value)
        all_sets.append(card_values)

    first_used_set = 0
    while first_used_set < len(all_sets) and len(all_sets[first_used_set]) == 0:
        first_used_set = first_used_set + 1

    card_sets = []
    set_index = first_used_set
    while set_index < len(all_sets) and len(all_sets[set_index]) > 0:
        card_sets.append(all_sets[set_index])
        set_index = set_index + 1
    return card_sets


def get_settings(world) -> dict:
    return {
        "seed": world.multiworld.seed_name,
        "floor_worlds": get_floor_worlds(world.world_order),
        "card_sets": get_card_sets(world.options),
        "attack_power": int(world.options.attack_power.value),
        "exp_multiplier": int(world.options.exp_multiplier.value),
    }


def get_mod_yml(settings: dict) -> str:
    return (
        f"title: KHRECOM Randomizer Seed {settings['seed']}\n"
        "originalAuthor: Gicu\n"
        "description: KHRECOM Randomizer Seed Information.  For use with gaithern/KHRECOM-RANDOMIZER\n"
        "assets:\n"
        "- name: scripts/io_packages/json/settings.json\n"
        "  method: copy\n"
        "  source:\n"
        "    - name: settings.json\n"
    )


def generate_seed_mod(world, output_directory: str) -> None:
    player_name = world.multiworld.get_file_safe_player_name(world.player)
    mod_name = f"AP-{world.multiworld.seed_name}-P{world.player}-{player_name}_{Utils.__version__}"
    settings = get_settings(world)
    files = {
        "settings.json": json.dumps(settings),
        "mod.yml": get_mod_yml(settings),
    }
    path = os.path.join(output_directory, mod_name + ".zip")
    seed_mod = KHRECOMSeedMod(files, path, world.player, world.multiworld.get_player_name(world.player))
    seed_mod.write()
