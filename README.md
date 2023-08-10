
# YAML to GitHub Output Action

This GitHub Action reads a YAML file containing key-value pairs and sends them to the GitHub Output file as environment variables in the format `key=value`. This allows you to dynamically set environment variables for subsequent steps in your GitHub Actions workflow. Optionally, you can filter the output based on a specific region key if your YAML file has nested dictionaries organized by regions keys.

## Usage

To use this action, follow these steps:

1. Create a `workflow.yml` file in your `.github/workflows` directory.

2. Add the following configuration to your workflow file:

```yaml
name: Your Workflow

on: [push, pull_request]

jobs:
  your_job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Run YAML to Github Output Action
      id: yaml-output
      uses: christian-ci/action-yaml-github-output@v1.0.0
      with:
        file_path: path/to/your_yaml_file.yaml
```

3. This action will read the specified YAML file, convert the key-value pairs into the desired format, and append them to the $GITHUB_OUTPUT file. You can then use these variables in subsequent steps of your GitHub Actions workflow.

## Inputs

| Name      | Description                                       | Required |
|-----------|---------------------------------------------------|----------|
| file_path | The relative path to the YAML file.               | Yes      |
| region    | (Optional) Filter the output based on this region.| No       |

## Example

Suppose you have a YAML file named `settings.yaml` with the following content:

```yaml
cluster-name: cluster1
app-name: yourapp
architecture: arm64
regions:
  us-west-1:
    cluster-name: us-cluster
    app-name: us-app
```

Using this action, you can convert these key-value pairs into environment variables and send them to the GitHub Output file.

Your workflow.yml file might look like this:

```yaml
name: Example Workflow

on: [push, pull_request]

jobs:
  example_job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Run YAML to Github Output Action
      id: yaml-output
      uses: christian-ci/action-yaml-github-output@v1.0.0
      with:
        file_path: path/to/settings.yaml
        region: us-west-1

    # Add subsequent steps that use the environment variables
```

After running this action with the region filter, the GitHub Output file will contain the following:

```bash
cluster-name=us-cluster
app-name=us-app
```

Without the region filter, the output would be:

```bash
cluster-name=cluster1
app-name=yourapp
architecture=arm64
```

Example of a step:

```yaml
name: Example Workflow

on: [push, pull_request]

jobs:
  example_job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Run YAML to Github Output Action
      id: yaml-output
      uses: christian-ci/action-yaml-github-output@v1.0.0
      with:
        file_path: path/to/settings.yaml

    - name: Use variables from output file
      env:
        ARCHITECTURE: ${{ steps.yaml-output.outputs.architecture }}
      run: |
        echo "Architecture: $ARCHITECTURE"
```