# UR Python Bootcamp - Technical Assignment

## Tech Stack

* Django
* pytest
* Celery
* PostgreSQL
* Ansible or Docker
* Bootstrap 3

## Scope

A web app where a User can **Signup** and **Login**, and where an Admin can **monitor** the queue of Signup Confirmation Emails. Here are the User Stories:

1. As a User, I want to land on a signup page and create an account.
2. As a User, I want to receive a signup confirmation email, so that I know that my account has been successfully created.
3. As a User, I want to be able to logout from the app.
4. As an Admin, I want to login the app back-office, so that I can monitor confirmation emails
5. As an Admin, I want to see a representation of the confirmation email *queue* (table view) with the proper ranking and status (*sent*, *trial-1*, *trial-2* etc…).
6. As an Admin, I want to be able to logout from the back-office.
7. Admin Dashboard should be updated real-time
8. Admin Dashboard should have a small real-time notification component where we display new entries notifications
9. Notification component entries should be stored within the DB 

## Deployment

Only `docker-compose` (and by extension `docker`) is required to run the app: [Install Docker Compose](https://docs.docker.com/compose/install/)

### To run the application:

    # docker-compose up

The application should then be available at `http://localhost:8000`

An admin user should be created when accessing `http://localhost:8000/admin` the first time. username=`admin` and password=`admin`

### To run the tests:

    # docker-compose -f docker-compose.yml -f docker-compose.tests.yml run pytest
