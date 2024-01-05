- [Project Shkedia/Worker Template](#project-shkediaworker-template)
- [Overview](#overview)
- [Deploy](#deploy)
  - [Build](#build)
- [Development](#development)
  - [Build](#build-1)
  - [Test](#test)
    - [Running Tests](#running-tests)


# Project Shkedia/Worker Template
# Overview
This repo is a suggested template for the workers in the shkedia project.  
It includes folder structure and basic configuration regarding the IDE and build processes.  

**Action to use template**
1. Update your requirements.txt
2. Update the variables names in the following files:
   1. README
   2. docker-compose
   3. server.properties
3. Update the entrypoint in the Dockerfile to fit your framework (in worker it's usually python3 main.py)
4. Set the development and production ports in the following files:
   1. docker-compose
   2. .devcontainer/devcontainer.json

# Deploy
## Build
First make sure all the changes are committed.
In the .autodevops/.cicd/ there is a script that does the following:
1. Bumps the project version if needed (using commitizen)
2. Updates the pip credentials
3. Builds the project image and tags it with the version

Go to the main folder of the project and run the following:
```bash
export ENV=dev0
bash .autodevops/.cicd/quick_build_deploy.sh {ENV}
```

# Development
## Build
The easiest way to start working with the project is to use vscode devcontainer extension.
For other IDEs check the .devcontainer for the development Dockerfile.  
Use the devcontainer.json in order to create the equivalent `docker run` command.

**IMPORTANT**: The Dockerfile searches for *.autodevops/.build/pip.conf* in order to install private packages. Make sure to supply it.

## Test
### Running Tests
1. Make sure you have all the requirements_dev.txt installed. It is essential for the tests
    ```bash
    pip install -r requirements_dev.txt
    ```
1. Run the tests using CLI
    ```bash
    pytest -s tests
    ```
**IMPORTANT**: Many of the tests need a connection to the sql server as they are integration tests.
**NOTE**: It is possible and easy to run the tests using VScode. Just press the "play" arrow. All the configuration for it are in the .vscode folder. Just make sure to install the Python Extension