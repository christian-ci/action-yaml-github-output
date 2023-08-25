import yaml
import os
import argparse

def extract_simple_nested(yaml_data, main_key=None, sub_key=None):
    if main_key:
        yaml_data = yaml_data.get(main_key, {})
    if sub_key:
        yaml_data = yaml_data.get(sub_key, {})
    return yaml_data

def extract_crud(yaml_data, top_level_keys=None, primary_key=None, primary_value=None):
    extracted_data = {}
    if top_level_keys is None:
        top_level_keys = yaml_data.keys()
    for key in top_level_keys:
        section_data = yaml_data.get(key, [])
        for entry in section_data:
            if entry.get(primary_key) == primary_value:
                extracted_data[key] = entry
    return extracted_data

def main_action():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True, help='Path to the yaml file')
    parser.add_argument('--main_key', help='Main key in the YAML to look for nested data', default=None)
    parser.add_argument('--sub_key', help='Sub key within the main key to extract data from', default=None)
    parser.add_argument('--format_type', help='The format of the YAML. Possible values: simple_nested, crud', default='simple_nested')
    parser.add_argument('--primary_key', help='Primary key in the CRUD format to look for specific settings block', default=None)
    parser.add_argument('--primary_value', help='Value of the primary key in the CRUD format to extract specific settings', default=None)
    parser.add_argument('--top_level_keys', type=str, help='Top-level keys to search in the YAML (Optional, comma-separated if multiple)')

    args = parser.parse_args()

    # Load YAML file
    with open(args.file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # Extract desired data
    if args.format_type == 'crud':
        top_level_keys = args.top_level_keys.split(",") if args.top_level_keys else None
        yaml_data = extract_crud(yaml_data, top_level_keys, args.primary_key, args.primary_value)
    else:
        yaml_data = extract_simple_nested(yaml_data, args.main_key, args.sub_key)

    # Get the GitHub env and output file paths from the environment variables
    github_env_file = os.environ.get('GITHUB_ENV')
    github_output_file = os.environ.get('GITHUB_OUTPUT')

    # Write data to the env and output files
    with open(github_env_file, 'a') as env_file, open(github_output_file, 'a') as output_file:
        for key, value in yaml_data.items():
            env_key = key.upper().replace('-', '_')
            env_file.write(f"{env_key}={value}\\n")
            output_file.write(f"{key}={value}\\n")

if __name__ == '__main__':
    try:
        main_action()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)