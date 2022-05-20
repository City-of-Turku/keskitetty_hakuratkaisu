import os, sys, yaml

def read_config(config_path):
    print(f"Reading configurations from config file...")
    conf_path = os.path.join(os.path.dirname(__file__), config_path)
    with open(conf_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as e:
            print(f"Reading configurations failed: {e}")
            sys.exit()        


# Returns all of the sections in the config file by the given key
def get_section_from_config_by_key(config, section_to_find, output = []):
    try:
        for (key, value) in config.items():
            if key == section_to_find:
                output.append(value)
            if isinstance(value, dict):
                get_section_from_config_by_key(value, section_to_find, output)
        return output
    except Exception  as e:
        print(f"Failed getting section from the configuration: {e}")
