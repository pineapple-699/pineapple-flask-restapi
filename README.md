# Pineapple Flask-REST-API
[![Build Status](https://travis-ci.com/pineapple-699/pineapple-flask-restapi.svg?branch=master)](https://travis-ci.com/pineapple-699/pineapple-flask-restapi)
[![codecov](https://codecov.io/gh/pineapple-699/pineapple-flask-restapi/branch/master/graph/badge.svg)](https://codecov.io/gh/pineapple-699/pineapple-flask-restapi)


## Development

This project is built with [Flask](https://flask.palletsprojects.com/en/1.1.x/). 

## Project Layout
| Key Folder | Parent Folder | Description |
| - | - | - |
| db | root | Holds the database and database creation tools | 
| models | root | Holds the main models and model methods for objects created in database | 
| endpoints | root | Holds the resources we use to create API endpoints | 

## Build 
### Install and create virtual environment library
```
cd python/
pip install virtualenv #if you don't have virtualenv installed 
```

Create virtualenv
```
virtualenv <Name_of_Virtual_Environment>
```

Activate virtualenv
```
source <Name_of_Virtual_Environment>/bin/activate
```
### Install project requirements
Install project requirements usings the requirements.text
```
pip install -r requirements.txt
```

## Run
Here are some quick commands to get started after install:

- `python ./db/database.py`: Creates database and populates it with fake data
- `python app.py`: Run flask application

## Endpoints
Active endpoints

GET /users _i.e. http://127.0.0.1:5000/users_

GET /users/name _i.e. http://127.0.0.1:5000/users/name_

DELETE /users/name 

POST /register

GET /products _i.e. http://127.0.0.1:5000/products_

GET /product/name _i.e. http://127.0.0.1:5000/product/name_

POST /product/name

GET /history/name _i.e. http://127.0.0.1:5000/history/name_

POST /shopping

POST /auth

## Resources
https://github.com/MaBlaGit/REST_API_Flask
