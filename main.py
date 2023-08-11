import yaml
import os
import argparse

def extract_simple_nested(yaml_data, main_key=None, sub_key=None):
    if main_key:
        yaml_data = yaml_data.get(main_key, {})
    if sub_key:
        yaml_data = yaml_data.get(sub_key, {})
    return yaml_data

def extract_crud(yaml_data, primary_key=None, primary_value=None):
    if not primary_key or not primary_value:
        return {}

    services = yaml_data.get('services', [])
    for service in services:
        if service.get(primary_key) == primary_value:
            return service
    return {}

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True, help='Path to the yaml file')
    parser.add_argument('--main_key', required=False, help='Main key in the YAML to look for nested data', default=None)
    parser.add_argument('--sub_key', required=False, help='Sub key within the main key to extract data from', default=None)
    parser.add_argument('--format_type', required=False, help='The format of the YAML. Possible values: simple_nested, crud', default='simple_nested')
    parser.add_argument('--primary_key', required=False, help='Primary key in the CRUD format to look for specific settings block', default=None)
    parser.add_argument('--primary_value', required=False, help='Value of the primary key in the CRUD format to extract specific settings', default=None)
    args = parser.parse_args()

    # Load YAML file
    yaml_file_path = args.file_path
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    primary_key = args.primary_key if hasattr(args, 'primary_key') else None
    primary_value = args.primary_value if hasattr(args, 'primary_value') else None
    if args.format_type == "crud":
        yaml_data = extract_crud(yaml_data, primary_key, primary_value)
    else:
        yaml_data = extract_simple_nested(yaml_data, args.main_key, args.sub_key)

    # Get the GitHub env and output file paths from the environment variables
    github_env_file = os.environ.get('GITHUB_ENV')
    github_output_file = os.environ.get('GITHUB_OUTPUT')

    # Iterate through the key-value pairs, write them to the env file, and collect them for outputs
    with open(github_env_file, 'a') as env_file:
        for key, value in yaml_data.items():
            # Convert key to uppercase and replace hyphens with underscores for environment variable naming convention
            env_key = key.upper().replace('-', '_')

            # Write to the env file
            env_line = f"{env_key}={value}\n"
            env_file.write(env_line)

            # Write to the output file without converting to uppercase
            output_line = f"{key}={value}\n"
            with open(github_output_file, 'a') as output_file:
                output_file.write(output_line)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
