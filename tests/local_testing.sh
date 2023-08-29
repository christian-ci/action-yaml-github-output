#!/bin/bash
echo "Local Testing for action-yaml-github-output"

# Set default values for GitHub environment variables
export GITHUB_ENV="github_env.txt"
export GITHUB_OUTPUT="github_output.txt"

# List of test files
declare -a test_files=("../.github/settings-simple-nested.yml" "../.github/settings-crud.yml" "../.github/settings-crud-top-level.yml")

# Loop through each test file
for file in "${test_files[@]}"; do
  echo "=================================================="
  echo "Running test with $file"

  # Remove previous GitHub environment files if they exist
  rm -f $GITHUB_ENV $GITHUB_OUTPUT

  # Determine format_type, primary_key, and primary_value based on the file name
  case $file in
    "../.github/settings-simple-nested.yml")
      python ../main.py --file_path=$file --main_key=regions --sub_key=us-west-1
      echo "---- Content of GITHUB_ENV ----"
      cat $GITHUB_ENV
      echo "-------------------------------"
      # Validate the output
      if grep -q "CLUSTER_NAME=us-cluster" $GITHUB_ENV && grep -q "APP_NAME=us-demo-app" $GITHUB_ENV; then
        echo "Test succeeded for $file"
      else
        echo "Test failed for $file"
      fi
      ;;
    "../.github/settings-crud.yml")
      python ../main.py --file_path=$file --format_type=crud --primary_key=app-name --primary_value=us-demo-app
      echo "---- Content of GITHUB_ENV ----"
      cat $GITHUB_ENV
      echo "-------------------------------"
      # Validate the output
      if grep -q "REGION=us-west-1" $GITHUB_ENV && grep -q "ACCEPTANCE_CLUSTER_NAME=us-cluster" $GITHUB_ENV; then
        echo "Test succeeded for $file"
      else
        echo "Test failed for $file"
      fi
      ;;
    "../.github/settings-crud-top-level.yml")
      python ../main.py --file_path=$file --format_type=crud --primary_key=app-name --primary_value=us-demo-app --top_level_keys=build,deployment
      echo "---- Content of GITHUB_ENV ----"
      cat $GITHUB_ENV
      echo "-------------------------------"
      # Validate the output
      if grep -q "PRE_PROD_CLUSTER_NAME=us-pre-cluster" $GITHUB_ENV && grep -q "PROD_CLUSTER_NAME=us-prod-cluster" $GITHUB_ENV; then
        echo "Test succeeded for $file"
      else
        echo "Test failed for $file"
      fi
      ;;
  esac
  echo "=================================================="
done
