# Homework 2 App

## Setup instructions
1. start a python virtual environment and activate
```sh
python -m venv .venv
source .venv/bin/activate
```
2. install dependencies
```sh
pip install -r requirements.txt
```
3. Run migrations
```sh
python manage.py migrate
```
4. start server
```sh
python manage.py runserver 0.0.0.0:8000
```