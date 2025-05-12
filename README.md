### Run tests with

```sh
python3 -m unittest discover tests
```

#### initial setup steps

```sh
python -m venv venv
source venv/bin/activate
pip install django djangorestframework psycopg2-binary
pip install django-stubs djangorestframework-stubs pydantic
django-admin startproject config .
python manage.py startapp api
```

#### migrations

```sh
python manage.py makemigrations

docker start db

python manage.py migrate
```
