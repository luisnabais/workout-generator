import yaml
import random
import questionary
from config_manager import load_config

def load_exercises(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def select_location(config):
    locations = config.get("locations", {})
    if not locations:
        print("No location set. Please edit exercises.yaml and config.yaml to add locations and equipment.")
        exit(1)
    print("Available locations:")
    loc_list = list(locations.keys())
    choice = questionary.select(
        "Choose location:",
        choices=[f"{loc} ({', '.join(locations[loc]['equipment'])})" for loc in loc_list]
    ).ask()
    # Extract location name
    selected_loc = choice.split(" (")[0]
    return selected_loc, locations[selected_loc]['equipment']

def list_categories(exercises):
    # Original main categories from YAML
    main_cats_from_yaml = list(exercises.keys())
    
    # Add virtual categories for full-body options
    virtual_cats = ["Full Body", "Full Body (No Core)"]
    main_cats = virtual_cats + main_cats_from_yaml
    
    # Subcategories remain the same (from YAML)
    sub_cats = []
    for main in main_cats_from_yaml:
        sub_cats.extend([f"{main}:{sub}" for sub in exercises[main]['subcategories'].keys()])
    
    return main_cats, sub_cats


def get_user_categories(main_cats, sub_cats):
    choices = []
    choices += [questionary.Choice(title=cat.title(), value=cat) for cat in main_cats]
    for cat in sub_cats:
        pretty = cat.split(":")[1].replace('_', ' ').title()
        main = cat.split(":")[0].title()
        choices.append(questionary.Choice(title=f"{pretty} ({main})", value=cat))
    selected = questionary.checkbox(
        "Select the categories for your workout:",
        choices=choices
    ).ask()
    return selected


def filter_exercises(exercises, available_equipment):
    filtered = {}
    for main_cat, data in exercises.items():
        filtered[main_cat] = {'subcategories': {}}
        for sub_cat, ex_list in data['subcategories'].items():
            valid_ex = []
            for ex in ex_list:
                if all(eq in available_equipment for eq in ex['equipment']):
                    valid_ex.append(ex)
            if valid_ex:
                filtered[main_cat]['subcategories'][sub_cat] = valid_ex
    return filtered

def generate_workout(exercises, selected):
    workout = {}
    for sel in selected:
        if sel == "Full Body":
            # Include one exercise from EVERY subcategory (upper, lower, core)
            for main_cat in ["upper", "lower", "core"]:
                if main_cat in exercises:
                    for sub_cat in exercises[main_cat]['subcategories']:
                        ex = random.choice(exercises[main_cat]['subcategories'][sub_cat])
                        workout[f"{main_cat}:{sub_cat}"] = ex
        elif sel == "Full Body (No Core)":
            # Include one exercise from EVERY subcategory (upper, lower only)
            for main_cat in ["upper", "lower"]:
                if main_cat in exercises:
                    for sub_cat in exercises[main_cat]['subcategories']:
                        ex = random.choice(exercises[main_cat]['subcategories'][sub_cat])
                        workout[f"{main_cat}:{sub_cat}"] = ex
        elif ':' in sel:
            # Existing subcategory logic
            main, sub = sel.split(':')
            ex = random.choice(exercises[main]['subcategories'][sub])
            workout[f"{main}:{sub}"] = ex
        else:
            # Existing main category logic
            for sub in exercises[sel]['subcategories']:
                ex = random.choice(exercises[sel]['subcategories'][sub])
                workout[f"{sel}:{sub}"] = ex
    return workout


def pretty_category(cat):
    main, sub = cat.split(':')
    return f"{main.title()} - {sub.replace('_', ' ').title()}"

def main():
    config = load_config()
    location, available_equipment = select_location(config)
    exercises = load_exercises('exercises.yaml')
    filtered_exercises = filter_exercises(exercises, available_equipment)
    main_cats, sub_cats = list_categories(filtered_exercises)
    selected = get_user_categories(main_cats, sub_cats)
    workout = generate_workout(filtered_exercises, selected)
    print(f"\nTreino para '{location}':")
    for cat, ex in workout.items():
        print(f"{pretty_category(cat)}: {ex['name']}")

if __name__ == "__main__":
    main()
