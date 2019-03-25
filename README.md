# Project 11: Pug or Ugh API

## Dependencies

* Python 3.6 or later
* Django 1.11.x LTS

Refer to requirements.txt

## To start

### 1. Initialize virtual environment to run the project

```
git clone https://github.com/nauticalist/techdegree-project11.git
cd techdegree-project11
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### 2. Start the server

```
python manage.py runserver
```
Browse http://127.0.0.1:8000 with your web browser.

### 3. Tests:

To run tests
```
coverage run manage.py test
```
![Tests](https://github.com/nauticalist/improve_menu_project/blob/master/screens/tests.png)
