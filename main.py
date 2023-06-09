import yaml
import os
import argparse

# Set up command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--file_path', required=True, help='Path to the yaml file')
args = parser.parse_args()

# Load YAML file
yaml_file_path = args.file_path
with open(yaml_file_path, 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Get the GitHub output file path from the environment variable
github_output_file = os.environ.get('GITHUB_OUTPUT')

# Iterate through the key-value pairs and write them to the output file
with open(github_output_file, 'a') as output_file:
    for key, value in yaml_data.items():
        output_line = f'{key}={value}\n'
        output_file.write(output_line)