import sys
import time
import cv2
import numpy as np
import pyautogui
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def read_resources():
    """
    Captures a screenshot, extracts a specific region, processes the image, and reads text using pytesseract.

    Returns:
    str: Extracted and processed text containing numeric information, potentially with the euro sign replaced with '6'.
    """

    def unsharp_mask(image, sigma=2, strength=1.6):
        """
        Applies unsharp mask to enhance edges in an image.

        Parameters:
        image (numpy.ndarray): Input image.
        sigma (int, optional): Standard deviation for Gaussian blur. Default is 2.
        strength (float, optional): Strength of the sharpening effect. Default is 1.8.

        Returns:
        numpy.ndarray: Sharpened image.
        """

        blurred = cv2.GaussianBlur(image, (0, 0), sigma)
        sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        return sharpened

    def preprocess_image(image):
        """
        Applies a series of image processing techniques to enhance text extraction.

        Parameters:
        image (numpy.ndarray): Input image.

        Returns:
        numpy.ndarray: Processed image ready for text extraction.
        """

        # Apply Unsharp Mask to sharpen edges
        sharpened_image = unsharp_mask(image)

        # Apply Bilateral Filter for edge-preserving smoothing
        bilateral_filtered = cv2.bilateralFilter(sharpened_image, d=9, sigmaColor=80, sigmaSpace=80)

        # Apply Global Thresholding
        _, binary_image = cv2.threshold(bilateral_filtered, 195, 255, cv2.THRESH_BINARY)

        # Apply Morphological Operations (Dilation followed by Erosion)
        kernel = np.ones((3, 3), np.uint8)
        morph_image = cv2.dilate(binary_image, kernel, iterations=1)
        morph_image = cv2.erode(morph_image, kernel, iterations=1)

        return morph_image

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Define the region you want to read (you can adjust the coordinates)
    region = (140, 960, 280, 1040)  # (top-left x, top-left y, bottom-right x, bottom-right y)

    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    # Crop the screenshot to the specified region
    cropped_screenshot = screenshot_np[region[1]:region[3], region[0]:region[2]]

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(cropped_screenshot, cv2.COLOR_BGR2GRAY)

    # Resize the image (optional, adjust the size as needed)
    resized_image = cv2.resize(grayscale_image, None, fx=4.5, fy=4.5)

    # Preprocess the image
    processed_image = preprocess_image(resized_image)

    # Read text from the processed image using pytesseract
    text = pytesseract.image_to_string(processed_image)

    # Check if the euro sign appears in the text
    if '€' in text:
        # Replace the euro sign with the number 6
        text = text.replace('€', '6')

    # Extract only digits using regular expressions
    digit_match = re.findall(r'\d+', text)

    # If digits are found, combine them
    if digit_match:
        text = ' '.join(digit_match)

    print('Resources:', text)
    return text


def get_resources():
    """
    Parses the resource information obtained from read_resources() and returns a dictionary
    containing the current and maximum values for health, mana, and stamina.

    Returns:
    - A dictionary with the following keys:
      - 'current_health': Current health value (integer).
      - 'max_health': Maximum health value (integer).
      - 'current_mana': Current mana value (integer).
      - 'max_mana': Maximum mana value (integer).
      - 'current_stamina': Current stamina value (integer).
      - 'max_stamina': Maximum stamina value (integer).
    """

    # Get resources information
    resources_info = read_resources()

    # Split the string into parts
    parts = resources_info.strip().split()

    # Create a dictionary to store the values
    resources_dict = {'current_health': 0, 'max_health': 0, 'current_mana': 0, 'max_mana': 0, 'current_stamina': 0,
                      'max_stamina': 0}

    # Check if there are enough parts

    if len(parts) == 6:
        resources_dict['current_health'] = int(parts[0])
        resources_dict['max_health'] = int(parts[1])
        resources_dict['current_mana'] = int(parts[2])
        resources_dict['max_mana'] = int(parts[3])
        resources_dict['current_stamina'] = int(parts[4])
        resources_dict['max_stamina'] = int(parts[5])
    else:
        print("***ERROR: Invalid number of parameters:", len(parts))

    return resources_dict


def check_if_ready_to_go():
    """
    Checks if the character is ready to resume the journey by examining the resources in a resting place.

    Returns:
    - ready_to_go: True if the character is ready to go, False otherwise.
    """

    ready_to_go = False

    while not ready_to_go:
        full_resources = check_resources_in_resting_place()
        if full_resources:
            print('Ready to go'),
            ready_to_go = True
        else:
            print("Not enough resources")
            pyautogui.press('r')
            time.sleep(30)

    return ready_to_go


def check_resources_in_resting_place():
    """
    Checks the character's resources in a resting place and performs error handling.

    Returns:
    - full_resources: True if all resources are full, False otherwise.
    """

    full_resources = False

    resources_dict = get_resources()
    is_dictionary_empty = all(value == 0 for value in resources_dict.values())
    if not is_dictionary_empty:
        if resources_dict['current_health'] > resources_dict['max_health'] or resources_dict['current_mana'] > \
                resources_dict['max_mana']:
            if resources_dict['current_health'] > resources_dict['max_health']:
                print('***Resources read health error handling in resting place...')
                pyautogui.press('r')
                time.sleep(30)
                full_resources = True

            elif resources_dict['current_mana'] > resources_dict['max_mana']:
                print('***Resources read mana error handling in resting place...')
                pyautogui.press('r')
                time.sleep(30)
                full_resources = True
        else:
            if resources_dict['current_health'] == resources_dict['max_health'] and resources_dict[
                'current_mana'] == resources_dict['max_mana'] and resources_dict['current_stamina'] == \
                    resources_dict['max_stamina']:
                print("Resources are full")
                full_resources = True

    else:
        print('***Resources read dictionary error handling in resting place...')
        pyautogui.press('r')
        time.sleep(30)
        full_resources = True

    return full_resources


def restore_health():
    """
    Performs actions to restore the character's health.
    """

    pyautogui.press('p')
    time.sleep(0.1)
    pyautogui.moveTo(1080, 765, duration=0.25)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.press('p')
    time.sleep(2)


def restore_mana():
    """
    Performs actions to restore the character's mana.
    """

    pyautogui.press('p')
    time.sleep(0.1)
    pyautogui.moveTo(1155, 765, duration=0.25)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.press('p')
    time.sleep(2)


def check_resources_in_boss_instance(enemy_name):
    """
    Checks the character's resources during a boss instance and performs error handling.

    Args:
    - enemy_name (str): The name of the boss.

    Returns:
    - health_potions_used: Number of health potions used during error handling (integer).
    - mana_potions_used: Number of mana potions used during error handling (integer).
    - number_of_repairs: Number of repairs needed during error handling (integer).
    """

    number_of_repairs = 0
    health_potions_used = 0
    mana_potions_used = 0
    while True:
        resources_dict = get_resources()
        is_dictionary_empty = all(value == 0 for value in resources_dict.values())
        if not is_dictionary_empty:
            print('Current hp:', resources_dict['current_health'], 'Current mana:', resources_dict['current_mana'])

            if enemy_name == 'Alpha':
                pass
            else:
                if resources_dict['current_health'] > resources_dict['max_health']:
                    print('***Resources read health error handling in boss instance...')
                    restore_health()
                    health_potions_used += 1
                    number_of_repairs += 1
                    continue
                else:
                    if (resources_dict['current_health']) < 600:
                        print('HEALTH level less than 600')
                        restore_health()
                        health_potions_used += 1
                        continue

                if resources_dict['current_mana'] > resources_dict['max_mana']:
                    print('***Resources read mana error handling in boss instance...')
                    restore_mana()
                    mana_potions_used += 1
                    number_of_repairs += 1
                    continue
                else:
                    if (resources_dict['current_mana']) < 450:
                        print('MANA level less than 450')
                        restore_mana()
                        mana_potions_used += 1
                        continue
            break
        else:
            if number_of_repairs < 2:
                print('***Resources read dictionary error handling in boss instance...')
                restore_mana()
                mana_potions_used += 1
                number_of_repairs += 1
                continue
            else:
                print('Resources read error handling reach max number of repairs in a single call!!!')
                sys.exit('Resources read error handling reach max number of repairs in a single call!!!')

    return health_potions_used, mana_potions_used, number_of_repairs


def find_grey_wolf_skin_in_inventory():
    """
    Searches for the grey wolf skin in the character's inventory.

    Returns:
    - True if the grey wolf skin is found in the inventory, False otherwise.
    """

    # Template path
    template_path = 'templates/equipment/grey_wolves_skin.PNG'

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
    threshold = 0.8

    # Check if the maximum match exceeds the threshold
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        # Get coordinates
        match_x, match_y = max_loc

        # Select an area
        h, w = template.shape
        cv2.rectangle(screenshot, (match_x, match_y), (match_x + w, match_y + h), (0, 255, 0), 2)

        print(f"Wolves skin found")

        # Hover over the center of the found area
        pyautogui.moveTo(match_x + w // 2, match_y + h // 2, duration=0.25)

        return True
    else:
        print(f"Wolves skin not found")
        return False


def find_burning_moonshine_in_inventory():
    """
    Searches for burning moonshine in the character's inventory.

    Returns:
    - True if burning moonshine is found in the inventory, False otherwise.
    """

    # Template path
    template_path = 'templates/equipment/burning_moonshine.PNG'

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
    threshold = 0.8

    # Check if the maximum match exceeds the threshold
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        # Get coordinates
        match_x, match_y = max_loc

        # Select an area
        h, w = template.shape
        cv2.rectangle(screenshot, (match_x, match_y), (match_x + w, match_y + h), (0, 255, 0), 2)

        print(f"Burning moonshine found")

        # Hover over the center of the found area
        pyautogui.moveTo(match_x + w // 2, match_y + h // 2, duration=0.25)

        return True
    else:
        print(f"Burning moonshine not found")
        return False


def remove_grey_wolf_skin_from_inventory():
    """
    Removes grey wolf skin from the character's inventory.
    """

    pyautogui.press('e')
    time.sleep(0.2)
    pyautogui.moveTo(680, 260, duration=0.25)
    pyautogui.click()

    skin_find = find_grey_wolf_skin_in_inventory()

    if skin_find:
        # Throw operation
        time.sleep(0.2)
        pyautogui.mouseDown()
        pyautogui.moveTo(180, 550, duration=0.25)
        pyautogui.mouseUp()
        pyautogui.moveTo(850, 660, duration=0.25)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.press('e')
        time.sleep(0.2)

        print('The wolf skin was thrown away')
    else:
        pyautogui.press('e')
        time.sleep(0.2)

        print('There are no wolf skin in the inventory')


def remove_burning_moonshine_from_inventory():
    """
    Removes burning moonshine from the character's inventory.
    """
    pyautogui.press('e')
    time.sleep(0.2)
    pyautogui.moveTo(680, 260, duration=0.25)
    pyautogui.click()

    burning_moonshine_find = find_burning_moonshine_in_inventory()

    if burning_moonshine_find:
        # Throw operation
        time.sleep(0.2)
        pyautogui.mouseDown()
        pyautogui.moveTo(180, 550, duration=0.25)
        pyautogui.mouseUp()
        pyautogui.moveTo(850, 660, duration=0.25)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.press('e')
        time.sleep(0.2)

        print('The burning moonshine was thrown away')
    else:
        pyautogui.press('e')
        time.sleep(0.2)

        print('There are no burning moonshine in the inventory')
