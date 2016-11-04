# Angular 2 Django seed project

A seed project for angular 2 and django using angular-cli.
Test django using py.test and angular using angular cli tests

## Getting started  

#### Prerequisites

  - [python](https://www.python.org/)
  - [npm](https://www.npmjs.com/)
  - [angular-cli](https://github.com/angular/angular-cli)

#### clone repo
```sh
git clone https://github.com/ashwinjv/seed-djangular2
```
#### create and activate virtualenv:
  - using python3 > 3.4: `python -m venv venv && source venv/bin/activate`
  - using virtualenv: `virtualenv venv && source venv/bin/activate`

#### Install necessary modules and packages
```
cd server
pip install -r requirements.txt
cd ../client
npm install
```

#### run server tests
```
cd server && py.test
```

#### run client tests
```
cd client && ng test --watch=false
```
`watch=false` to run the test once.

#### run e2e tests
build angular2 dist
```
cd client
ng build
```
start django
```
cd server
python mange.py runserver
```
Run e2e angular tests in another terminal
```
cd client
ng e2e
```
