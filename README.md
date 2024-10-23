# BBHMM

### Splitwise Clone API

## Instructions for venv

### Create a virtual environment
`python3 -m venv bbhmm-env`

### Activate
`source bbhmm-env/bin/activate`

### Deactivate
`deactivate`

### Update dependency list
`pip freeze > requirements.txt`

### Install from dependency list
`pip install -r requirements.txt`

## Instructions for Docker

### Build the docker image
`docker build --platform linux/arm64 --tag python-docker .`

### Run the image as a container
`docker run -d -p 5000:5000 python-docker`

## Intructions for development

### Create the Flask app in app directory
`flask run --debug`

## Instructions for testing

### Run all tests from the app directory
`python -m pytest ..`

### Run unit tests from the app directory
`python -m pytest -m unit ..`

### Run integration tests from the app directory
`python -m pytest -m integration ..`