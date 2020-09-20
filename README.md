# TODO Application

TODO is an application intented to keep and manage your tasks(bonus: Email notifications)

## Description

Application allows to Create, Read, Retrieve, Update and Delete tasks. To proceed this actions user must own the tasks i.e. user must be the one who created them.

Application requires a user to be authorized to use the endpoints, so there is a Register and Login functions. Authorization is done by using JsonWebTokens.

Also, there is an endpoint that allows to mark the task as "Done" or "Undone". After an execution of this action, user receives an email that informs him about it. This feature was developed using Celery and Redis

Additionally, default Django user model was altered to fit the needs of the application


## Stack
Django, Django Rest Framework, Redis, Celery, SQLite
