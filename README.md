# Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Installation

```bash
pip install -r requirements.txt
```
## Deployment
The Casting Agency API is deployed on Render. You can access the API using the following link:

https://casting-agency-vraf.onrender.com 


Before running the API, make sure to set the required environment variables:


```bash
  set FLASK_APP=app.py
  set FLASK_ENV=development
```
To start the API, use the following command:
```
  python -m flask run 
```

## API Documentation
The Casting Agency API provides the following endpoints:

Actors
- GET /actors: Retrieve a list of all actors.
- POST /actors: Create a new actor.
- PATCH /actors/<actor_id>: Update an existing actor.
- DELETE /actors/<actor_id>: Delete an existing actor.

Movies
- GET /movies: Retrieve a list of all movies.
- POST /movies: Create a new movie.
- PATCH /movies/<movie_id>: Update an existing movie.
- DELETE /movies/<movie_id>: Delete an existing movie.

## RBAC and User Roles
The API implements Role-Based Access Control (RBAC) with the following user roles:

1- Casting Assistant
  - Can view actors and movies

2- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies

3- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database


Casting Director:

 - POST /actors
 - PATCH /actors/<actor_id>
 - PATCH /movies/<movie_id>
 - DELETE /actors/<actor_id>

Executive Producer:
 - POST /actors
 - POST /movies
 - PATCH /actors/<actor_id>
 - PATCH /movies/<movie_id>
 - DELETE /actors/<actor_id>
 - DELETE /movies/<movie_id>

Please note that the ```GET / ```and ```GET /actors``` and ```GET /movies``` endpoints don't require authentication.


Example commands using curl:
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d '{"name":"Dwayne Johnson","age":51,"gender":"Male","movie_id":1}' https://casting-agency-vraf.onrender.com/actors
```
