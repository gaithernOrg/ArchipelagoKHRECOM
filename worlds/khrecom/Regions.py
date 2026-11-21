from typing import Dict, List

from BaseClasses import Entrance, Region
from .Locations import KHRECOMLocation, KHRECOMLocationData, location_table


REGION_EXITS: Dict[str, List[str]] = {
    "Menu":                  ["Traverse Town"],
    "Traverse Town":         ["Castle Oblivion Halls"],
    "Wonderland":            [],
    "Olympus Coliseum":      [],
    "Monstro":               [],
    "Agrabah":               [],
    "Halloween Town":        [],
    "Atlantica":             [],
    "Neverland":             [],
    "Hollow Bastion":        [],
    "100 Acre Wood":         [],
    "Twilight Town":         [],
    "Destiny Islands":       [],
    "Castle Oblivion":       [],
    "Heartless":             [],
    "Levels":                [],
    "Castle Oblivion Halls": ["Wonderland", "Olympus Coliseum", "Monstro", "Agrabah", "Halloween Town",
                              "Atlantica", "Neverland", "Hollow Bastion", "100 Acre Wood", "Twilight Town",
                              "Destiny Islands", "Castle Oblivion", "Heartless", "Levels"],
}


def is_location_active(khrecomworld, location_data: KHRECOMLocationData) -> bool:
    if location_data.option == "":
        return True
    return bool(getattr(khrecomworld.options, location_data.option))


def get_active_locations(khrecomworld) -> Dict[str, KHRECOMLocationData]:
    active: Dict[str, KHRECOMLocationData] = {}
    for name, data in location_table.items():
        if is_location_active(khrecomworld, data):
            active[name] = data
    return active


def create_regions(khrecomworld):
    player = khrecomworld.player
    regions = {name: Region(name, player, khrecomworld.multiworld) for name in REGION_EXITS}

    for name, data in get_active_locations(khrecomworld).items():
        region = regions[data.region]
        region.locations.append(KHRECOMLocation(player, name, data.code, region))

    for name, exits in REGION_EXITS.items():
        for exit_name in exits:
            regions[name].exits.append(Entrance(player, exit_name, regions[name]))

    khrecomworld.multiworld.regions += regions.values()


def connect_entrances(khrecomworld):
    for exits in REGION_EXITS.values():
        for exit_name in exits:
            khrecomworld.get_entrance(exit_name).connect(khrecomworld.get_region(exit_name))
