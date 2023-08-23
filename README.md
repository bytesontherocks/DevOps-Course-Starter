# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

Please add the following Trello credentials in the .env file
TRELLO_API_KEY=
TRELLO_API_TOKEN=
TRELLO_BOARD_ID=

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Testing
You can run all the test using 'poetry run pytest' 

You can run individual test with any of the vscode pluggins e.g. Test Explorer and selecting the appropriate test.

## Deploying web service to a managed node
In the ansible directory you can find the playbook to deploy the flask application into a managed node and automatically run it. The playbook will prompt you to provide the trello credentials. Edit the inventory file to define the managed node IP.

## Running the application in Docker
Create the container image ```  docker build -t todo-app .   ```
Run it ```  docker run -p 8000:8000 --env-file .env -it todo-app ```
Bind the docker container port 8000 to the host port 8000 and pass the keys through the .env file.

### Multi stage

``` 
docker build --target prod -t todo-app:prod .       
docker run --env-file ./.env -p 8000:8000 -it todo-app:prod
```

In dev we worked in the app mapped version from the host to see changes.
```
docker build --target dev -t todo-app:dev .       
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/web_app/todo_app -it todo-app:dev
```

In test
```
docker build --target test --tag my-test-image .
docker run my-test-image ./todo_app/tests
```


## Using Docker compose
Alternative to run the long docker run instruction for development the docker compose file can be used: ``` docker compose up ```
## General docker actions
To delete all containers including its volumes use: ``` docker rm -vf $(docker ps -aq) ```
To delete all the images: ``` docker rmi -f $(docker images -aq)  ```

## Generating architecture documentation
Install PlantUML from Jebbs in VSCode (https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)

You can render the diagrams locally (ALT + D) or export them using different formats.

To configure the export files, add the following lines in the .vscode/settings.json

```
"plantuml.diagramsRoot": "documentation/architecture",
"plantuml.exportOutDir": "documentation/architecture/out"
```

## Azure manual deployment

Docker image: 
```
docker.io/bytesontherocks/todo-app:latest
docker pull bytesontherocks/todo-app:latest
```

Set of instructions run for Azure cli:

``` shell
# create plan
az appservice plan create --resource-group resource_group_example -n exercice_m8 --sku B1 --is-linux

# create app and provide a name for the web app
az webapp create --resource-group resource_group_example --plan exercice_m8 --name bytesontherocks-m8 --deployment-container-image-name docker.io/bytesontherocks/todo-app:prod

# set up environment variables
az webapp config appsettings set -g resource_group_example -n bytesontherocks-m8 --settings @.env.json

# re-direct listening port
az webapp config appsettings set --resource-group resource_group_example --name bytesontherocks-m8 --settings WEBSITES_PORT=8000
```