import yaml

def load_config(filepath='config/sources.yml'):
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    return config