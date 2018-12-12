# double_entry
## Overview
Proof of concept double-entry accounting REST API backend.

## Requirements
* Ununtu 
* Postgres 

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
Create `./.env` file with `SECRET_KEY` e.g.
```dotenv
SECRET_KEY=p8*sya*g@6)rwh*=*sev3u3t4z9p9o#t*k3h+fgx-0=6d@fhk3

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
python manage.py makemigrations
python manage.py migrate
```

## Providing initial data
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
 
#Drawbacks (TODO)
 - No user authentication yet.
 - No data filtering implemented (e.g. django-filter).
 - No Admin Site
 - No Swagger support yet (e.g. drf-yasg, django-rest-swagger)
 - Using SQLite, no PostgreSQL configured yet for easy demo launch.
 - Not enough documentation
