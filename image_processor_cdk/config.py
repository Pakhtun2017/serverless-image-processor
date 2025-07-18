import yaml


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)
