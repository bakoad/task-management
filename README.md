# Task Manager API

## Table of Contents

* Getting Started
* API Endpoints
* Creating a Task
* Listing Tasks
* Retrieving a Task
* Updating a Task
* Deleting a Task

## Getting Started

To start using the Task Manager API, follow these steps:

1. Clone the repository and navigate into the cloned folder.
2. Run `docker compose build` to build the Docker image.
3. Run `docker compose up` to start the API.

The API will be available at http://localhost:8000. You can view the API documentation at http://localhost:8000/redoc.

## API Endpoints

### Creating a Task

To create a new task, send a POST request to http://localhost:8000/tasks/ with a JSON payload containing the task details.

curl -X POST http://localhost:8000/tasks/ -H 'Content-Type: application/json' -d '{"title": "Create api", "description": "Create the task manager api", "due_date": "2025-06-20", "status": "PENDING"}'

The response will contain the created task with a unique id.

{
  "title": "Create api",
  "description": "Create the task manager api",
  "due_date": "2025-06-20",
  "status": "PENDING",
  "id": 2,
  "creation_date": "2025-06-01T13:41:07"
}

### Listing Tasks

To retrieve a list of tasks, send a GET request to http://localhost:8000/tasks/.

```bash
curl -X GET "http://localhost:8000/tasks/"
```
You can filter tasks by status, due_date, and order_by using query parameters.

```bash
curl -X GET "http://localhost:8000/tasks/?status=PENDING&due_date=2025-06-22&order_by=-creation_date"
```
### Retrieving a Task

To retrieve a single task, send a GET request to http://localhost:8000/tasks/<id>.
```bash
curl -X GET "http://localhost:8000/tasks/2"
```
### Updating a Task

To update a task, send a PUT request to http://localhost:8000/tasks/<id> with a JSON payload containing the updated task details.
```bash
curl -X PUT http://localhost:8000/tasks/2 -H 'Content-Type: application/json' -d '{"title": "Create api8", "description": "Create the task manager api", "due_date": "2025-06-22", "status": "PENDING"}'
```
### Deleting a Task

To delete a task, send a DELETE request to http://localhost:8000/tasks/<id>.
```bash
curl -X DELETE "http://localhost:8000/tasks/2"
```
