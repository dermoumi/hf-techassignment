# Python Technical Assignment 🙂

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

## Bonus Scope

1. Admin Dashboard should be updated real-time
2. Admin Dashboard should have a small real-time notification component where we display new entries notifications
3. Notification component entries should be stored within the DB 
