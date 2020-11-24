# LinkedOutServer

Backend server for LinkedOutApp (2021I_INT3120_1 class project)

## Prepare Database (MySql)

Install MySql database, then create database and grant permissions.

```sql
CREATE DATABASE backend CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'backend'@'%' IDENTIFIED BY 'backend';
GRANT ALL PRIVILEGES ON backend.* TO 'backend'@'%';
FLUSH PRIVILEGES;
```

## Prepare environment for backend application

On Linux

```bash
export DJANGO_DATABASE_HOST="localhost"
export DJANGO_DATABASE_NAME="backend"
export DJANGO_DATABASE_USER="backend"
export DJANGO_DATABASE_PASSWORD="backend"
export DJANGO_CONFIG_SECRETKEY="ihateyou"
```

On Windows

Go to Search -> type "env" -> `Edit the system environment variables` -> `Environment Variables...` -> `New...` -> Add the 5 variables above.

## Installing dependencies

```bash
python -m pip install -r requirements.txt
```

## Database migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create superuser account for admin site

```bash
python manage.py createsuperuser
```

You will be prompted to enter a username, email address, and strong password.


## Running server

```bash
python manage.py runserver
```


## Sample data
Sample data can be found [here](https://drive.google.com/file/d/1cNSVeVk8bPR3z8l2FUc8r4v4HPm9esHK/view?usp=sharing)
