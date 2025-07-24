import yaml

def load_config_file():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config