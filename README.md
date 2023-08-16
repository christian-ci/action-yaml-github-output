
# YAML to GitHub Output Action

This GitHub Action reads a YAML file containing key-value pairs and sends them to the GitHub Output as step outputs. In addition, it sets them as environment variables following the conventional UPPERCASE format.

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
      uses: christian-ci/action-yaml-github-output@v3.1
      with:
        file_path: path/to/your_yaml_file.yaml
```

3. This action will read the specified YAML file, convert the key-value pairs into the desired format, and append them as step outputs. They will also be available as environment variables in the conventional UPPERCASE format for subsequent steps in your GitHub Actions workflow.

## Inputs

| Name          | Description                                        | Required | Default         |
|---------------|----------------------------------------------------|----------|-----------------|
| file_path     | The relative path to the YAML file.                | Yes      |                 |
| format_type   | The format of the YAML. Possible values: `simple_nested`, `crud`. | No | `simple_nested` |
| main_key      | Main key in the YAML to look for nested data.     | No       | None            |
| sub_key       | Sub key within the main key to extract data from. | No       | None            |
| primary_key   | Primary key for the CRUD format.                  | No       | None            |
| primary_value | Primary value for the CRUD format.                | No       | None            |

## Example

### Simple Nested

Suppose you have a YAML file named `settings.yaml` with the following content:

```yaml
app-name: demo-app
architecture: arm64
regions:
  us-west-1:
    cluster-name: us-cluster
    app-name: us-demo-app
  eu-central-1:
    cluster-name: eu-cluster
    app-name: eu-demo-app
```

Using this action, you can convert these key-value pairs into step outputs and environment variables.

Your `workflow.yml` file might look like this:

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
      uses: christian-ci/action-yaml-github-output@v3.1
      with:
        file_path: path/to/settings.yaml
        main_key: regions
        sub_key: us-west-1

    - name: Print Variables
      run: |
        echo "Cluster Name: ${{ env.CLUSTER_NAME }}"
        echo "App Name: ${{ env.APP_NAME }}"

    - name: Print Outputs
      run: |
        echo "Cluster Name: ${{ steps.yaml-output.outputs.cluster-name }}"
        echo "App Name: ${{ steps.yaml-output.outputs.app-name }}"    
```

### CRUD

For the `crud` format, the YAML file might look like:

```yaml
services:
  - app-name: us-demo-app
    region: us-west-1
    acceptance-cluster-name: us-cluster
    pre-prod-cluster-name: us-pre-cluster
    prod-cluster-name: us-prod-cluster

  - app-name: eu-demo-app
    region: eu-central-1
    cluster-name: eu-cluster
    architecture: arm64
```

In this case, you can specify the `primary_key` and `primary_value` to fetch specific settings. For example, if you want to extract the settings for the `us-demo-app`, you can set `primary_key` to `app-name` and `primary_value` to `us-demo-app`.

Your `workflow.yml` file might look like:

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
      uses: christian-ci/action-yaml-github-output@v3.1
      with:
        file_path: path/to/settings.yaml
        format_type: crud
        primary_key: app-name
        primary_value: us-demo-app

    - name: Print Variables
      run: |
        echo "Cluster Name: ${{ env.CLUSTER_NAME }}"
        echo "App Name: ${{ env.APP_NAME }}"

    - name: Print Outputs
      run: |
        echo "Cluster Name: ${{ steps.yaml-output.outputs.cluster-name }}"
        echo "App Name: ${{ steps.yaml-output.outputs.app-name }}"    
```