import yaml

def load_config():
    """Loading config.yaml file."""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            if config is None:
                print("Error: 'config.yaml' is empty or badly formatted.")
                exit()
            return config
    except FileNotFoundError:
        print("Error: 'config.yaml' not found.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading config.yaml: {e}")
        exit()