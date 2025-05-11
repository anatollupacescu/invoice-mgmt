### Run tests with

```sh
python3 -m unittest discover tests
```

#### initial setup steps

```sh
python -m venv venv
source venv/bin/activate
pip install django djangorestframework psycopg2-binary
django-admin startproject config .
python manage.py startapp api
```
