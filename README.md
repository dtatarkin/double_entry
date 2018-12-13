# double_entry
## Overview
Proof of concept double-entry accounting REST API backend.

## Requirements
* Ununtu 
* PostgreSQL 

## Installation

### Install pyenv 
https://github.com/pyenv/pyenv#installation

### Install Python 

Installation of `libffi-dev` required due bug
https://github.com/pyenv/pyenv/issues/1183#issuecomment-402546470

```bash
sudo apt-get install libffi-dev
pyenv install 3.7.1
```

### Install `pipenv`

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
python3 -m pip install --user pipenv

```

### Clone git repository
```bash
git clone https://github.com/dtatarkin/double_entry.git
cd double_entry
```

### Install dependancies
```bash
pipenv install
```

## Build docs
```bash
sphinx-apidoc --doc-project double_entry --output-dir ./docs/apidoc . ./*/migrations ./manage.py accounts/tests/ postings/tests
sphinx-build  ./docs ./docs/_build
```

## Linting
Config file: `./prospector.yaml` 
```bash
prospector
```

## Configure
Create `./.env` see `.env.example` e.g.
```dotenv
SECRET_KEY=<SECRET_KEY>
POSTGRES_DATABASE=double_entry
POSTGRES_USER=double_entry
POSTGRES_PASSWORD=double_entry
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```
## Generate migrations
```bash
python manage.py makemigrations
```

## Run tests
```bash
pytest
```
with coverage report:
```bash
pytest --cov=.
```

## Initialize Database
```bash
python manage.py migrate
```

## Provide initial data
```bash
python manage.py loaddata users.json
python manage.py loaddata accounts.json
```

## Run server
```bash
python manage.py runserver
```
## Browseble api
 - [List of Accounts](http://127.0.0.1:8000/accounts/accounts/)
 - [Payments List And Create](http://127.0.0.1:8000/payments/payments/)
 
# Drawbacks (TODO)
 - No user authentication yet.
 - No data filtering implemented (e.g. django-filter).
 - No Admin Site
 - No Swagger support yet (e.g. drf-yasg, django-rest-swagger)
 - Not enough documentation
