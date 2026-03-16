# UpWork Freelance App (Django MVT)

## Project Description

This project is a freelance marketplace web application inspired by Upwork.
It allows clients to post projects and freelancers to submit bids for those projects.

Clients can review freelancer proposals, accept or reject bids, and once a bid is accepted a contract is created between the client and the freelancer.

The application is built using Django MVT architecture and includes authentication, project management, bidding, and contract functionality.

---

## Features

* User authentication (Register/Login)
* Client can create and manage projects
* Freelancers can browse projects and submit bids
* Clients can accept or reject bids
* Automatic contract creation after bid acceptance
* Project status management
* User profile system

---

## Technologies Used

* Python
* Django
* Django Templates (MVT architecture)
* Django ORM
* SQLite / PostgreSQL
* HTML
* CSS
* Bootstrap

---



## Test Users

Client

```
username: client1
password: client123
```

Freelancer

```
username: freelancer1
password: freelancer123
```

---

## Installation Guide

### 1 Clone the repository

```
git clone https://github.com/jasminnurmanova/UpWork-freelance-app.git
```

### 2 Go to project directory

```
cd UpWork-freelance-app
```

### 3 Create virtual environment

```
python -m venv venv
```

### 4 Activate virtual environment

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

### 5 Install dependencies

```
pip install -r requirements.txt
```

### 6 Run migrations

```
python manage.py migrate
```

### 7 Run the server

```
python manage.py runserver
```

### 8 Open in browser

```
http://127.0.0.1:8000
```

---

## Author

Jasmin Nurmanova
GitHub: https://github.com/jasminnurmanova
POSTMAN: https://documenter.getpostman.com/view/51287189/2sBXigNEGX