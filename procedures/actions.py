import time
import cv2
import pyautogui
import numpy as np


def check_cave():
    """
    Checks the current location for a cave entrance.

    Returns:
    - The name of the found cave entrance if detected, or "You are not in the boss instance" if not found.
    """

    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    img_screen = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    img_river_cave = cv2.imread('templates/caves/river_cave.PNG', cv2.IMREAD_GRAYSCALE)
    img_canyon_cave = cv2.imread('templates/caves/canyon_cave.PNG', cv2.IMREAD_GRAYSCALE)
    img_right_cave = cv2.imread('templates/caves/right_cave.PNG', cv2.IMREAD_GRAYSCALE)

    def compare_images(template, target, threshold=0.8):
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        return locations

    def find_cave_entrance(screen, cave_templates, cave_names):
        found_cave = None  # Variable storing the name of the found cave
        for i, template in enumerate(cave_templates):
            locations = compare_images(template, screen)

            if len(locations[0]) > 0:
                found_cave = cave_names[i]
                for pt in zip(*locations[::-1]):
                    cv2.rectangle(screen, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

        return found_cave

    # Prepare a list of templates for each cave
    cave_templates = [img_river_cave, img_canyon_cave, img_right_cave]

    # Prepare a list of cave names in the correct order
    cave_names = ["river_cave", "canyon_cave", "right_cave"]

    # Find and mark cave entrances on the current screen
    found_cave = find_cave_entrance(img_screen, cave_templates, cave_names)

    # Print the name of the found cave (if found)
    if found_cave:
        return found_cave
    else:
        return "You are not in the boss instance"


def enter_alpha_cave():
    """
    Attempts to enter the Alpha cave by detecting the cave entrance on the screen.

    Returns:
    - True if the cave entrance is found and successfully clicked, False otherwise.
    """

    # Default file paths
    template_path = 'templates/entrance_to_the_cave/cave_entrance.PNG'

    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Search for a template match
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if the maximum match exceeds the threshold
    threshold = 0.7
    if max_val >= threshold:
        # Get coordinates
        match_x, match_y = max_loc

        # Select an area
        h, w = template.shape
        cv2.rectangle(screenshot, (match_x, match_y), (match_x + w, match_y + h), (0, 255, 0), 2)

        print(f"Cave entrance found at position ({match_x}, {match_y})")

        # Hover over the center of the found area
        pyautogui.moveTo(match_x + w // 2, match_y + h // 2, duration=0.25)

        # Wait and click
        time.sleep(1)
        pyautogui.rightClick()

        return True
    else:
        print("Cave enrance not found.")
        return False


def move_to_checkpoint(checkpoint_name, template_path, threshold, x_offset, y_offset):
    """
    Moves the character to a specified checkpoint based on a template match in the screen image.

    Args:
    - checkpoint_name (str): The name of the checkpoint for identification.
    - template_path (str): The file path to the template image for the checkpoint.
    - threshold (float): The confidence level threshold for the template match.
    - x_offset (int): The horizontal offset to adjust the mouse hover position.
    - y_offset (int): The vertical offset to adjust the mouse hover position.
    """

    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Search for a combat template match in the screen image
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Check if the maximum match exceeds the threshold
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        # Get coordinates
        match_x, match_y = max_loc

        # Select an area
        h, w = template.shape
        cv2.rectangle(screenshot, (match_x, match_y), (match_x + w, match_y + h), (0, 255, 0), 2)

        print(f"{checkpoint_name} found")

        # Hover over the center of the found area
        pyautogui.moveTo(match_x + w - x_offset // 2, match_y + h - y_offset // 2, duration=0.25)

        # Wait and click
        time.sleep(1)
        if checkpoint_name == "Exit checkpoint":
            pyautogui.rightClick()
        else:
            pyautogui.click()

    else:
        print(f"{checkpoint_name} not found")


def move_to_resting_area():
    """
    Moves the character to the resting area by detecting the resting place entrance on the screen.

    Returns:
    - True if the resting place entrance is found and successfully clicked, False otherwise.
    """

    # Default file paths
    template_path = 'templates/entrance_to_the_cave/resting_place.PNG'

    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Search for a combat template match in the screen image
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Set the match threshold
    threshold = 0.7

    # Check if the maximum match exceeds the threshold
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        # Get coordinates
        match_x, match_y = max_loc

        # Select an area
        h, w = template.shape
        cv2.rectangle(screenshot, (match_x, match_y), (match_x + w, match_y + h), (0, 255, 0), 2)

        print("Resting place found")
        x_offset = 300
        y_offset = 100
        # Hover over the center of the found area
        pyautogui.moveTo(match_x + w - x_offset // 2, match_y + h - y_offset // 2, duration=0.25)

        # Wait and click
        time.sleep(1)
        pyautogui.click()
        return True
    else:
        print("Resting place not found")
        return False
