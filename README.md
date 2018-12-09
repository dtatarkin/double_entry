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
sphinx-apidoc --doc-project double_entry --output-dir ./docs/apidoc . ./*/migrations ./manage.py
sphinx-build  ./docs ./docs/_build
```

## Linting
Config file: `./prospector.yaml` 
```bash
prospector
```

## Running tests
```bash
pytest
```
