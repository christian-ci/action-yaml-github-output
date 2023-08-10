import yaml
import os
import argparse

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', required=True, help='Path to the yaml file')
    parser.add_argument('--main_key', required=False, help='Main key in the YAML to look for nested data', default=None)
    parser.add_argument('--sub_key', required=False, help='Sub key within the main key to extract data from', default=None)
    args = parser.parse_args()

    # Load YAML file
    yaml_file_path = args.file_path
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # If main_key and sub_key are specified, filter data for those keys
    if args.main_key and args.sub_key:
        yaml_data = yaml_data.get(args.main_key, {}).get(args.sub_key, {})

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