# Microservice for Search Index of Phone Numbers

# What is it

Microservice listens remote database for new rows which are orders for call center. It writes rows into local database and adds new column for standartized phone number.
# What in use
- sqlaclchemy
- alembic
# How to
## 1. Install requirements
```sh
$ pip install -r requirements
```
## 2. Create backup from remote db and restore it on local with pgAdmin4
## 3. Create environment variable for database url
```sh
$ export DATABASE_URL=your_url
```
## 4. Create db migration with alembic
```sh
$ alembic update head
```
## 5. Run script
```sh
$ python load_orders_to_local_db.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
