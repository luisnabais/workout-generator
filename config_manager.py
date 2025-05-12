import yaml
import os

CONFIG_FILE = "config.yaml"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"locations": {}}
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file)
