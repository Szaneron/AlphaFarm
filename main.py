import os
import sys
import time
from procedures.actions import enter_alpha_cave, check_cave
from procedures.combat import check_if_in_combat, combat_handling
from caves_handling.right_cave_handling import right_cave_path
from caves_handling.river_cave_handling import river_cave_path
from procedures.resources import remove_burning_moonshine_from_inventory, check_if_ready_to_go
from caves_handling.canyon_cave_handling import canyon_cave_path

ALPHA_KILLED = 0
HEALTH_POTIONS_USED = 0
MANA_POTIONS_USED = 0
POTIONS_ERROR_OCCURS = 0


def show_global_info():
    """
    Display global information including the number of Alpha kills, HP potions used,
    Mana potions used, and potions error occurrences.
    """

    print('--------------------------')
    print('ALPHA KILLED:', ALPHA_KILLED)
    print('HEALTH POTIONS USED:', HEALTH_POTIONS_USED)
    print('MANA POTIONS USED:', MANA_POTIONS_USED)
    print('POTIONS ERROR:', POTIONS_ERROR_OCCURS)
    print('--------------------------')


# Start time of the program
start_time = time.time()

try:
    for approach in range(1, 31):
        time.sleep(2)
        ready_to_go, health_potions, mana_potions, potions_error = check_if_ready_to_go()
        HEALTH_POTIONS_USED += health_potions
        MANA_POTIONS_USED += mana_potions
        POTIONS_ERROR_OCCURS += potions_error

        start_loop_time = time.time()

        print('--------------------------')
        print('APPROACH NUMBER:', approach)
        print('--------------------------')

        while True:
            entrance_to_the_cave = enter_alpha_cave()
            if entrance_to_the_cave:
                time.sleep(7)
                in_combat = check_if_in_combat()

                if in_combat:
                    enemy_name = combat_handling()
                elif not in_combat:
                    print(f'The player has reached the entrance')
                    break

        current_cave = check_cave()

        print('Current cave:', current_cave)
        match current_cave:
            case 'river_cave':
                health_potions, mana_potions, potions_error = river_cave_path()
                HEALTH_POTIONS_USED += health_potions
                MANA_POTIONS_USED += mana_potions
                POTIONS_ERROR_OCCURS += potions_error
                ALPHA_KILLED += 1
            case 'canyon_cave':
                health_potions, mana_potions, potions_error = canyon_cave_path()
                HEALTH_POTIONS_USED += health_potions
                MANA_POTIONS_USED += mana_potions
                POTIONS_ERROR_OCCURS += potions_error
                ALPHA_KILLED += 1
            case 'right_cave':
                health_potions, mana_potions, potions_error = right_cave_path()
                HEALTH_POTIONS_USED += health_potions
                MANA_POTIONS_USED += mana_potions
                POTIONS_ERROR_OCCURS += potions_error
                ALPHA_KILLED += 1

        remove_burning_moonshine_from_inventory()
        show_global_info()

        loop_time = round(time.time() - start_loop_time)
        minutes, seconds = divmod(loop_time, 60)
        print(f"Time of approach number {approach}: {int(minutes)} min, {int(seconds)} sec")
        print()

        time.sleep(15)

except Exception as e:
    print(f"Exception occurred: {e}")

finally:
    show_global_info()

    total_time = round(time.time() - start_time)
    total_minutes, total_seconds = divmod(total_time, 60)
    print(f"Total working time: {int(total_minutes)} min, {int(total_seconds)} sec")
    print("The program has been terminated")

    input("Naciśnij Enter, aby zakończyć program.")
