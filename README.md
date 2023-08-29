
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
      uses: christian-ci/action-yaml-github-output@v2
      with:
        file_path: path/to/your_yaml_file.yaml
```

3. This action will read the specified YAML file, convert the key-value pairs into the desired format, and append them as step outputs. They will also be available as environment variables in the conventional UPPERCASE format for subsequent steps in your GitHub Actions workflow.

## Inputs

| Name          | Description                                        | Required | Default         |
|---------------|----------------------------------------------------|----------|-----------------|
| file_path     | The relative path to the YAML file.                | Yes      |                 |
| format_type   | The format of the YAML. Possible values: `simple_nested`, `crud`. | No | `simple_nested` |
| main_key      | Main key in the YAML to look for nested data.      | No       | None            |
| sub_key       | Sub key within the main key to extract data from.  | No       | None            |
| primary_key   | Primary key for the CRUD format.                   | No       | None            |
| primary_value | Primary value for the CRUD format.                 | No       | None            |
| top_level_keys | Top-level keys to search in the YAML (Optional, comma-separated if multiple). | No | All top-level keys |

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
      uses: christian-ci/action-yaml-github-output@v2
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
build:
- app-name: us-demo-app
  dockerfile: Dockerfile
- app-name: eu-demo-app
  dockerfile: path/Dockerfile
deployment:
- app-name: us-demo-app
  pre-prod-cluster-name: us-pre-cluster
  acceptance-cluster-name: us-cluster
  prod-cluster-name: us-prod-cluster
  region: us-west-1

- app-name: eu-demo-app
  architecture: arm64
  cluster-name: eu-cluster
  region: eu-central-1
```

In this case, you can specify the `top_level_keys`, `primary_key` and `primary_value` to fetch specific settings. For example, if you want to extract the settings for the `us-demo-app`, you can set `primary_key` to `app-name` and `primary_value` to `us-demo-app`.

Your `workflow.yml` file might look like:

```yaml
name: Comprehensive Example Workflow

on: [push, pull_request]

jobs:
  comprehensive_example_job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Run YAML to Github Output Action for 'build' settings
      id: yaml-output-build
      uses: christian-ci/action-yaml-github-output@v2
      with:
        file_path: path/to/settings.yaml
        format_type: crud
        top_level_keys: build
        primary_key: app-name
        primary_value: us-demo-app

    - name: Run YAML to Github Output Action for 'deployment' settings
      id: yaml-output-deployment
      uses: christian-ci/action-yaml-github-output@v2
      with:
        file_path: path/to/settings.yaml
        format_type: crud
        top_level_keys: deployment
        primary_key: app-name
        primary_value: us-demo-app

    - name: Print Variables from 'build' settings
      run: |
        echo "Dockerfile Path: ${{ env.DOCKERFILE }}"
        echo "App Name: ${{ env.APP_NAME_BUILD }}"

    - name: Print Outputs from 'build' settings
      run: |
        echo "Dockerfile Path: ${{ steps.yaml-output-build.outputs.dockerfile }}"
        echo "App Name: ${{ steps.yaml-output-build.outputs.app-name }}"

    - name: Print Variables from 'deployment' settings
      run: |
        echo "Pre-prod Cluster: ${{ env.PRE_PROD_CLUSTER_NAME }}"
        echo "Prod Cluster: ${{ env.PROD_CLUSTER_NAME }}"
        echo "Region: ${{ env.REGION }}"

    - name: Print Outputs from 'deployment' settings
      run: |
        echo "Pre-prod Cluster: ${{ steps.yaml-output-deployment.outputs.pre-prod-cluster-name }}"
        echo "Prod Cluster: ${{ steps.yaml-output-deployment.outputs.prod-cluster-name }}"
        echo "Region: ${{ steps.yaml-output-deployment.outputs.region }}"
```