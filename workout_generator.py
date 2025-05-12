import yaml
import random
import questionary
import os
from config_manager import load_config

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")  # [1][2]

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def load_exercises(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def select_location(config):
    locations = config.get("locations", {})
    if not locations:
        print("No locations defined. Add them in config.yaml.")
        exit(1)
    
    choice = questionary.select(
        "Select location:",
        choices=[
            f"{name} ({', '.join(data['equipment'])})"
            for name, data in locations.items()
        ]
    ).ask()
    selected_name = choice.split(" (")[0]
    return selected_name, locations[selected_name]["equipment"]

def filter_exercises(exercises, available_equipment):
    filtered = {}
    for category, subs in exercises["categories"].items():
        filtered[category] = {}
        for sub, ex_list in subs.items():
            valid = [
                ex for ex in ex_list
                if all(eq in available_equipment for eq in ex["equipment"])
            ]
            if valid:
                filtered[category][sub] = valid
    return filtered

def get_virtual_categories(data):
    return list(data["virtual_categories"].keys())

def generate_workout(filtered_exercises, virtual_cat_def, selected_cats):
    workout = {}
    
    # First build group-to-base mapping dynamically
    group_to_base = {}
    for base_cat, subs in filtered_exercises.items():
        for sub in subs.keys():
            group_to_base[sub] = base_cat
    
    for cat in selected_cats:
        config = virtual_cat_def[cat]
        
        if "include_all_from" in config:
            # Handle categories like Full Body, Core
            for base_cat in config["include_all_from"]:
                if base_cat in filtered_exercises:
                    for sub, ex_list in filtered_exercises[base_cat].items():
                        if ex_list:
                            workout[f"{base_cat}:{sub}"] = random.choice(ex_list)
        
        elif "include_groups" in config:
            # Handle Upper, Lower, Push, Pull
            for group in config["include_groups"]:
                base_cat = group_to_base.get(group)
                if not base_cat:
                    continue  # Skip unrecognized groups
                
                if base_cat in filtered_exercises:
                    ex_list = filtered_exercises[base_cat].get(group, [])
                    if ex_list:
                        workout[f"{base_cat}:{group}"] = random.choice(ex_list)
    
    return workout


def main():
    config = load_config()
    location, equipment = select_location(config)
    debug_print(f"\nAvailable equipment in {location}: {equipment}")

    data = load_exercises("exercises.yaml")
    filtered = filter_exercises(data, equipment)
    debug_print("\nFiltered exercises structure:")
    debug_print(yaml.dump(filtered))
    
    virtual_cats = data["virtual_categories"]
    selected = questionary.checkbox(
        "Select workout type(s):",
        choices=list(virtual_cats.keys())
    ).ask()
    
    workout = generate_workout(filtered, virtual_cats, selected)
    
    print(f"\nWorkout for {location}:")
    for category, exercise in workout.items():
        base, sub = category.split(":")
        print(f"{base.title()} - {sub.replace('_', ' ').title()}: {exercise['name']}")

if __name__ == "__main__":
    main()
