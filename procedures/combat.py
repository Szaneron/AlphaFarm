import cv2
import numpy as np
import pyautogui
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def check_if_in_combat():
    """
    Checks if the player is in combat by examining the enemy name.

    Returns:
    - True if the player is in combat.
    - False if the player is not in combat.
    """

    enemy_name = check_enemy_name()
    if enemy_name:
        print("The player is in combat.")
        return True

    else:
        print("The player is not in combat.")
        return False


def check_if_still_in_combat():
    """
    Checks if the player is still in combat by examining the enemy name.

    Returns:
    - True if the player is still in combat.
    - False if the player is no longer in combat.
    """

    enemy_name = check_enemy_name()
    if enemy_name:
        return True

    else:
        return False


def check_enemy_name():
    """
    Takes a screenshot of a specified region, processes the image to extract enemy name,
    and returns the detected text.

    Returns:
    - A string containing the detected enemy name.
    """

    def unsharp_mask(image, sigma=1.0, strength=1.5):
        blurred = cv2.GaussianBlur(image, (0, 0), sigma)
        sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        return sharpened

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Define the region you want to read (you can adjust the coordinates)
    region = (1350, 920, 1480, 960)  # (top-left x, top-left y, bottom-right x, bottom-right y)

    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    # Crop the screenshot to the specified region
    cropped_screenshot = screenshot_np[region[1]:region[3], region[0]:region[2]]

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(cropped_screenshot, cv2.COLOR_BGR2GRAY)

    # Resize the image (optional, adjust the size as needed)
    resized_image = cv2.resize(grayscale_image, None, fx=5, fy=5)

    # Apply Unsharp Mask to sharpen edges
    sharpened_image = unsharp_mask(resized_image)

    # cv2.imwrite('new.png', sharpened_image)

    # Apply Global Thresholding
    _, binary_image = cv2.threshold(sharpened_image, 200, 255, cv2.THRESH_BINARY)

    # Apply Morphological Operations (Dilation followed by Erosion)
    kernel = np.ones((3, 3), np.uint8)
    morph_image = cv2.dilate(binary_image, kernel, iterations=1)
    morph_image = cv2.erode(morph_image, kernel, iterations=1)

    # Read text from the processed image using pytesseract
    text = pytesseract.image_to_string(morph_image).strip()

    return text


def combat_with_enemy(enemy_name):
    """
    Engages in combat with a specified enemy based on the enemy's name.

    Args:
    - enemy_name (str): The name of the enemy to engage in combat with.

    Returns:
    None
    """

    combat_in_progress = True
    if enemy_name == 'Wilk Czarny' or enemy_name == 'Wilczyca':
        pyautogui.press('4')
        time.sleep(0.2)
        pyautogui.press(' ')
        time.sleep(0.2)
        pyautogui.press('2')

        while combat_in_progress:
            result = check_if_still_in_combat()
            print('In combat:', result)

            if not result:
                print('End of combat')
                break

            time.sleep(3)

        time.sleep(2)
        pyautogui.press('esc')

    elif enemy_name == 'Alpha':
        pyautogui.press('3')
        time.sleep(0.2)
        pyautogui.press(' ')
        time.sleep(0.2)
        pyautogui.press('2')

        while combat_in_progress:
            result = check_if_still_in_combat()
            print('In combat:', result)

            if not result:
                print('End of combat')
                break

            time.sleep(3)

        time.sleep(2)
        pyautogui.press('esc')

    elif enemy_name == 'Kold':
        pyautogui.press('2')
        time.sleep(0.2)
        pyautogui.press(' ')

        while combat_in_progress:
            result = check_if_still_in_combat()
            print('In combat:', result)

            if not result:
                print('End of combat')
                break

            time.sleep(3)

        time.sleep(2)
        pyautogui.press('esc')


def combat_handling():
    """
    Handles combat with detected enemies.

    Returns:
    - String: Enemy name.
    """

    enemy_name = check_enemy_name()
    print('Enemy:', enemy_name)
    combat_with_enemy(enemy_name)

    return enemy_name
