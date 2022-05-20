from config_model import ValidationModel
from pydantic import ValidationError
import os
import sys
import yaml


def read_config(config_path):
    print(f"Reading configurations from config file...")
    conf_path = os.path.join(os.path.dirname(__file__), config_path)
    config = {}
    with open(conf_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(f"Reading configurations failed: {e}")
            sys.exit()
    
    try:
        ValidationModel.parse_obj(config)
    except ValidationError as e:
        print(f'Configuration validation failed:\n{e}')
        sys.exit()

    return config


# Return specific configs to ui
def get_ui_configs(config):
    configs_to_return = {}
    try:
        # Analytics - location: backend.analytics
        configs_to_return['analytics'] = get_section_from_config_by_key(config, 'analytics', [])[0] # array in array
        # Languages - location: elasticsearch.languages
        configs_to_return['languages'] = get_section_from_config_by_key(config, 'languages', [])[0] # array in array
        # Content types - location: under each spider
        content_types = get_section_from_config_by_key(config, 'CONTENT_TYPES_AND_THEMES', [])
        content_types = remove_key_from_dict(content_types, 'settings')
        content_type_keys = get_keys_from_dict(content_types)
        content_type_keys = list(dict.fromkeys(content_type_keys))
        
        configs_to_return['content_types'] = content_type_keys
    
    except Exception as e:
        print(f"Problem: {e}") 

    return configs_to_return


# Returns all of the sections in the config file by the given key
# Does not go inside lists
def get_section_from_config_by_key(config, section_to_find, output = []):
    config = config
    try:
        for (key, value) in config.items():
            if key == section_to_find:
                output.append(value)
            if isinstance(value, dict):
                get_section_from_config_by_key(value, section_to_find, output)
        return output
    except Exception as e:
        print(f"Failed getting section from the configuration: {e}")


# Remove settings from content types
def remove_key_from_dict(dic, key_to_remove):
    for x in dic:
        for k in x.keys():  
            if(k == key_to_remove):
                del x[k]
                break
    return dic


# Return only keys from dict:
def get_keys_from_dict(dic):
    dict_keys = []
    for x in dic:
        if isinstance(x, dict):
            for k in x.keys():
                dict_keys.append(k)
    return dict_keys
