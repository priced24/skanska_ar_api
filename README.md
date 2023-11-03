# Smart Campus API

## Local Setup
Setting up the application for development first involves creating a virtual environment and installing the dependencies using `pip`.

### Pre-requisites
Before setting up the application locally, first ensure that you have `Python3` and `pip` installed.

### Creating a Virtual Environment
A virtual environment can be created using the following command (ensure you are in the correct directory before executing it):

`python3 -m venv .venv`

This will create a new directory called `.venv` that will manage the application's dependencies and environment.

Before installing the application dependencies, first activate the virtual environment (the following command is for Linux based systems):

`source .venv/bin/activate`

The command is similar for other operating systems. Once run, `(.venv)` should appear on the left of your terminal line. Running `deactivate` will deactivate the virtual environment.

### Installing Dependencies
After activating the virtual envrionment, dependencies specified in `requirements.txt` can be installed with:

`pip install -r requirements.txt`

## Initializing the Database
Before running and using the application, the database needs to be iniatialized. This can be done in two ways:

1. &nbsp;&nbsp;&nbsp;&nbsp;`flask --app api init_db`
   
   This will create a `db.sqlite` file in the `instance` directory, that is initialized with empty tables corresponding to the models defined in `models.py`.

2. &nbsp;&nbsp;&nbsp;&nbsp;`flask --app api init_db --dummy`

    This will similarly create a `db.sqlite` file in the `instance` directory, that is initialized with data specified in `test_data.json` in the `test_data` directory.

    Documentation on modifying the `test_data.json` is located in [`test_data/TESTDATA.md`](/api/test_data/TESTDATA.md)

## Running the Application
The application can be run in debug mode using the following command:

`flask --app api --debug run`