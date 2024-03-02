from procedures.actions import move_to_checkpoint
from procedures.actions import move_to_resting_area
from procedures.resources import check_resources_in_boss_instance, remove_grey_wolf_skin_from_inventory
from procedures.combat import check_if_in_combat, combat_handling
import time

first_checkpoint = ['First checkpoint', 'templates/river_cave/first_checkpoint.PNG']
second_checkpoint = ['Second checkpoint', 'templates/river_cave/second_checkpoint.PNG']
third_checkpoint = ['Third checkpoint', 'templates/river_cave/third_checkpoint.PNG']
boss_checkpoint = ['Boss checkpoint', 'templates/river_cave/boss_checkpoint.PNG']
exit_checkpoint = ['Exit checkpoint', 'templates/river_cave/exit_checkpoint.PNG']


def river_cave_path():
    """
    Executes a predefined path through the river cave, interacting with checkpoints and handling combat.

    Returns:
    - The usage statistics of health and mana potions, as well as the occurrence of errors during potion usage.

    Checkpoints:
    - first checkpoint
    - second checkpoint
    - third checkpoint
    - boss checkpoint
    """

    potions_error_occurs = 0
    health_potions_used = 0
    mana_potions_used = 0
    checkpoint_list = ['first checkpoint', 'second checkpoint', 'third checkpoint', 'boss checkpoint']

    for checkpoint in checkpoint_list:
        while True:
            if checkpoint == 'first checkpoint':
                move_to_checkpoint(first_checkpoint[0], first_checkpoint[1], 0.6, 430, 170)
            elif checkpoint == 'second checkpoint':
                move_to_checkpoint(second_checkpoint[0], second_checkpoint[1], 0.6, 50, 140)
            elif checkpoint == 'third checkpoint':
                move_to_checkpoint(third_checkpoint[0], third_checkpoint[1], 0.6, 0, 0)
            elif checkpoint == 'boss checkpoint':
                move_to_checkpoint(boss_checkpoint[0], boss_checkpoint[1], 0.6, 0, 70)

            time.sleep(3)
            in_combat = check_if_in_combat()

            if in_combat:
                enemy_name = combat_handling()

                if enemy_name == 'Alpha':
                    break

                health_potions, mana_potions, potions_error = check_resources_in_boss_instance(enemy_name)
                health_potions_used += health_potions
                mana_potions_used += mana_potions
                potions_error_occurs += potions_error

            elif not in_combat:
                if checkpoint == 'third checkpoint':
                    remove_grey_wolf_skin_from_inventory()

                print(f'The player has reached the {checkpoint}')
                break

    back_to_cave_enter_from_boss(third_checkpoint, second_checkpoint, first_checkpoint, exit_checkpoint)

    while True:
        while True:
            resting_place_found = move_to_resting_area()
            if resting_place_found:
                break
            time.sleep(5)

        time.sleep(4)
        in_combat = check_if_in_combat()

        if in_combat:
            combat_handling()
        elif not in_combat:
            print(f'The player has reached the resting area')
            break

    print('River cave route ended')
    return health_potions_used, mana_potions_used, potions_error_occurs


def back_to_cave_enter_from_boss(third_checkpoint, second_checkpoint, first_checkpoint, exit_checkpoint):
    """
    Navigates the character back through a predefined path from the boss area to the cave entrance.

    Parameters:
    - third_checkpoint (List): Coordinates and template path for the third checkpoint.
    - second_checkpoint (List): Coordinates and template path for the second checkpoint.
    - first_checkpoint (List): Coordinates and template path for the first checkpoint.
    - exit_checkpoint (List): Coordinates and template path for the exit checkpoint.
    """

    checkpoint_list = ['third checkpoint', 'second checkpoint', 'first checkpoint', 'exit checkpoint']

    for checkpoint in checkpoint_list:
        while True:
            if checkpoint == 'third checkpoint':
                move_to_checkpoint(third_checkpoint[0], third_checkpoint[1], 0.6, 0, 0)
            elif checkpoint == 'second checkpoint':
                move_to_checkpoint(second_checkpoint[0], second_checkpoint[1], 0.6, 50, 140)
            elif checkpoint == 'first checkpoint':
                move_to_checkpoint(first_checkpoint[0], first_checkpoint[1], 0.6, 430, 170)
            elif checkpoint == 'exit checkpoint':
                move_to_checkpoint(exit_checkpoint[0], exit_checkpoint[1], 0.6, 400, 150)

            time.sleep(3)
            in_combat = check_if_in_combat()

            if in_combat:
                combat_handling()

            elif not in_combat:
                print(f'The player has reached the {checkpoint}')
                break
