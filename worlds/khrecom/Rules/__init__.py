from rule_builder.rules import Has, Rule

from . import exit_halls, heartless, levels, rooms_of_rewards, worlds


def build_location_rules(khrecomworld) -> dict[str, Rule]:
    location_rules: dict[str, Rule] = {}
    location_rules.update(rooms_of_rewards.build_rules())
    location_rules.update(exit_halls.build_rules())
    location_rules.update(levels.build_rules(khrecomworld))
    location_rules.update(heartless.build_rules())
    location_rules.update(worlds.build_rules())
    return location_rules


def get_active_location_names(khrecomworld) -> set[str]:
    return {location.name for location in khrecomworld.multiworld.get_locations(khrecomworld.player)}


def set_rules(khrecomworld) -> None:
    active_location_names = get_active_location_names(khrecomworld)
    for name, rule in build_location_rules(khrecomworld).items():
        if name in active_location_names:
            khrecomworld.set_rule(khrecomworld.get_location(name), rule)
    for name, rule in worlds.build_entrance_rules().items():
        khrecomworld.set_rule(khrecomworld.get_entrance(name), rule)
    khrecomworld.set_completion_rule(Has("Victory"))
