# Custom Workout Generator in Python

This project is a simple and extensible application for generating personalized workouts from a categorized list of exercises, taking into account available equipment and workout location.

---

## Features

- Exercise list organized into categories and subcategories (e.g., vertical pull, horizontal push, anterior/posterior legs, core, etc.).
- Exercises annotated with required equipment (pull-up bar, dumbbells, kettlebell, parallel bars, bodyweight, etc.).
- Configuration of locations (e.g., home, gym) with available equipment for each.
- Workout generation automatically filtered according to the equipment available at the selected location.
- Simple text interface for selecting categories and location.
- Data structure in YAML for easy editing and maintenance.

---

## Project Structure

- `exercises.yaml`: Contains the exercise list, organized by categories and subcategories, with associated equipment.
- `config.yaml`: Configuration file containing workout locations and the equipment available at each.
- `workout_generator.py`: Main script to generate workouts, interacting with the user via the terminal.
- `config_manager.py`: Helper functions to load and save YAML configurations.

---

## How to Use

### Prerequisites

- Python 3.7+
- Libraries: `pyyaml` and `questionary` for interactive menus (install with `pip install -r requirements.txt`)

### Steps

1. Edit `exercises.yaml` to adjust or add exercises as you like.
2. Use `admin.py` to add workout locations and available equipment:
