import yaml
import os
import argparse

def write_to_files(data_dict, env_file, output_file):
    with open(env_file, 'a') as env_f, open(output_file, 'a') as out_f:
        for key, value in data_dict.items():
            env_key = key.upper().replace('-', '_')
            env_f.write(f"{env_key}={value}\n")
            out_f.write(f"{key}={value}\n")

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
        top_level_keys = [None]

    for top_level_key in top_level_keys:
        if top_level_key:
            yaml_data_filtered = yaml_data.get(top_level_key, [])
        else:
            yaml_data_filtered = yaml_data

        if not primary_key or not primary_value:
            output[top_level_key] = yaml_data_filtered
            continue

        items_list = yaml_data_filtered if isinstance(yaml_data_filtered, list) else []
        for item in items_list:
            if item.get(primary_key) == primary_value:
                output[top_level_key] = item
                break

    return output

def main_action():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True, help='Path to the yaml file')
    parser.add_argument('--main_key', default=None)
    parser.add_argument('--sub_key', default=None)
    parser.add_argument('--format_type', default='simple_nested')
    parser.add_argument('--primary_key', default=None)
    parser.add_argument('--primary_value', default=None)
    parser.add_argument('--top_level_keys', default=None)
    args = parser.parse_args()

    with open(args.file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    if args.format_type == "crud":
        yaml_data = extract_crud(yaml_data, args.primary_key, args.primary_value, args.top_level_keys)
    else:
        yaml_data = extract_simple_nested(yaml_data, args.main_key, args.sub_key)

    github_env_file = os.environ.get('GITHUB_ENV')
    github_output_file = os.environ.get('GITHUB_OUTPUT')

    if isinstance(yaml_data, dict):
        for top_level_key, nested_data in yaml_data.items():
            if isinstance(nested_data, dict):
                write_to_files(nested_data, github_env_file, github_output_file)
            else:
                write_to_files({top_level_key: nested_data}, github_env_file, github_output_file)
    else:
        write_to_files(yaml_data, github_env_file, github_output_file)

if __name__ == "__main__":
    try:
        main_action()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
