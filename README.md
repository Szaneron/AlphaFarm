# Alpha Farm Bot
AlphaFarm is a Python script designed to automate the process of obtaining items from a specific boss in order to sell it on the market and earn gold in Broken Ranks. The script leverages computer vision and automation to streamline movement, combat, and resource management.

Broken Ranks is a Polish production - the successor to The Pride of Taern. This title is in the top of the best games MMORPG in Poland. The game stands out mainly because of: a unique combat system, a dark and realistic world, a non-linear plot,open world and a rich character development system.


## Table of Contents
- [Informations](#informations)
- [Branches](#branches)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Actions](#actions)
- [Project Structure](#project-structure)
- [Visual presentation](#visual-presentation)
- [Requirements](#requirements)

## Informations
- The script prints all executed actions in the console, which makes it possible to observe its correct operation and to find a potential error.
- The script is designed for a resolution of 1920x1080, it will not work properly on any other resolution.
- Additionally, the game must be in windowed mode, not fullscreen mode. To achieve this, just click f11 in the game.
- The game window must be maximized to the entire screen.
- The program performs mouse movements and clicks, reads the player's position and controls various situations, it is not recommended to use the mouse or keyboard for your own purposes.
- The game window cannot be covered with anything.

## Branches 
The repository has two active branches.
- master: Contains code adapted to be run by the IDE
- exe_branch: The code has been changed to include all its functionalities in a single executable file. Branch also contains a ready-made exe file in the dict folder.

## Features
- Automated navigation through specific cave instances (River Cave, Right Cave, Canyon Cave).
- Combat handling with different enemies, such as Alpha, Wilk Czarny, Wilczyca and Kold.
- Efficient usage of health and mana potions during combat encounters.
- Inventory management, including the removal of specific items (e.g., Grey Wolf Skin).
- Support for various checkpoints within each cave instance.
- Automatic return at the beginning of the boos instance with the exit from the cave
- Finding and reaching places where the character can rest and regenerate his resources.

## Getting Started
Follow the steps below to get started with AlphaFarm.

### Prerequisites
Make sure you have the following software installed on your system:
- Python 3.11
- Tesseract OCR: [Download Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Szaneron/AlphaFarm.git
    cd AlphaFarm
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set the path to your Tesseract OCR executable in the settings.py file:
    ```bash
    pytesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    ```

## Actions
Program actions step by step (in short):
- Check if the resources are full before entering the cave.
- Find the entrance and enter the boss instance.
- Check which cave was drawn.
- Run the specific cave handling script based on your current location:
  - river_cave_handling.py for the River Cave
  - right_cave_handling.py for the Right Cave
  - canyon_cave_handling.py for the Canyon Cave
- The script will navigate through checkpoints, engage in combat, and manage resources automatically.
- Kill the boss, return to the beginning of the instance and exit the cave.
- Find a place to rest to replenish your resources before moving on again.

## Project Structure
The project structure is organized as follows:
- settings.py: Configuration file for setting paths and constants.
- procedures: Contains modules for different actions:
  - actions.py: Module for managing character movements (e.g., moving to checkpoints, move to resting area, enter alpha cave).
  - combat.py: Combat management module (e.g., check enemy name, cobat handling).
  - resources.py: Resource management module (e.g., read resources, restore mana, remove grey wolf skin from inventory).
- caves_handling: Contains modules that support the passage through a specific cave:
  - canyon_cave_handling.py: Canyon cave passage handling module.
  - river_cave_handling.py: River cave passage handling module.
  - right_cave_handling.py: Right cave passage handling module.
- templates: Includes image templates for cave entrances, checkpoints, and other elements.
- main.py: The main program code connecting all modules.


## Visual presentation
Videos presenting the operation of the program.

<details> 
<summary> Entrance to the cave and the path to the first checkpoint with combat handling </summary>
  
https://github.com/Szaneron/AlphaFarm/assets/58951668/f0388680-8d9a-4b6f-833e-b6bed808d984
</details>

<details> 
  <summary> Combat handling </summary>
    
  https://github.com/Szaneron/AlphaFarm/assets/58951668/fa7158c5-d35b-4a16-99c9-07026f14ddeb
</details>

<details> 
  <summary> Back to the entrance of the cave </summary>
  
  https://github.com/Szaneron/AlphaFarm/assets/58951668/f36f6fea-a696-46a7-801a-eadc6392881d
</details>

<details> 
  <summary> Move to resting area after leaving boss instance to restore resources </summary>
  
  https://github.com/Szaneron/AlphaFarm/assets/58951668/602cf9d8-f417-4aa8-b395-fc09b2c797af
</details>


## Requirements
- opencv-python~=4.9.0.80
- numpy~=1.26.4
- PyAutoGUI~=0.9.54
- pytesseract~=0.3.10
