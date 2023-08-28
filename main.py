import yaml
import os
import argparse

def extract_simple_nested(yaml_data, main_key=None, sub_key=None):
    if main_key:
        yaml_data = yaml_data.get(main_key, {})
    if sub_key:
        yaml_data = yaml_data.get(sub_key, {})
    return yaml_data

def extract_crud(yaml_data, primary_key=None, primary_value=None, top_level_keys=None):
    output = {}
    if top_level_keys:
        top_level_keys = top_level_keys.split(',')
    else:
        # Dynamically detect the top-level keys
        if isinstance(yaml_data, dict) and len(yaml_data.keys()) == 1:
            top_level_keys = list(yaml_data.keys())
        else:
            top_level_keys = [None]

    for top_level_key in top_level_keys:
        if top_level_key:
            yaml_data_filtered = yaml_data.get(top_level_key, [])
        else:
            yaml_data_filtered = yaml_data

        if not primary_key or not primary_value:
            output[top_level_key] = yaml_data_filtered
            continue

        services = yaml_data_filtered if isinstance(yaml_data_filtered, list) else []
        for service in services:
            if service.get(primary_key) == primary_value:
                output[top_level_key] = service
                break

    return output

def main_action():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True, help='Path to the yaml file')
    parser.add_argument('--main_key', help='Main key in the YAML to look for nested data', default=None)
    parser.add_argument('--sub_key', help='Sub key within the main key to extract data from', default=None)
    parser.add_argument('--format_type', help='The format of the YAML. Possible values: simple_nested, crud', default='simple_nested')
    parser.add_argument('--primary_key', help='Primary key in the CRUD format to look for specific settings block', default=None)
    parser.add_argument('--primary_value', help='Value of the primary key in the CRUD format to extract specific settings', default=None)
    parser.add_argument('--top_level_keys', help='Top-level keys for the CRUD format (Optional, comma-separated)', default=None)
    args = parser.parse_args()

    with open(args.file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    if args.format_type == "crud":
        yaml_data = extract_crud(yaml_data, args.primary_key, args.primary_value, args.top_level_keys)
    else:
        yaml_data = extract_simple_nested(yaml_data, args.main_key, args.sub_key)

    github_env_file = os.environ.get('GITHUB_ENV', 'env.txt')
    github_output_file = os.environ.get('GITHUB_OUTPUT', 'output.txt')

    with open(github_env_file, 'a') as env_file, open(github_output_file, 'a') as output_file:
        for key, value in yaml_data.items():
            env_key = key.upper().replace('-', '_')
            env_file.write(f"{env_key}={value}\n")
            output_file.write(f"{key}={value}\n")

if __name__ == "__main__":
    try:
        main_action()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
