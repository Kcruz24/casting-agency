# Casting Agency

## Motivation
What motivated me to do this project was the opportunity to put into practice all
that I have learned in the Full Stack Web Dev nanodegree program from Udacity. I created a stand-alone REST API
which I'm proud of, and I learned more about the authentication side in this
project. At the time I only did the REST API without a front-end because I'm busy
with other things, but I will be getting back to this and add the frontend as well as
some other features that I have in mind. Overall, I really liked this experience,
and I would do it again. In fact, I have some projects in mind that I want to do
that will be possible thanks to what I learned in this nanodegree program.

### POV
The Casting Agency models a company that is responsible for creating movies and
managing and assigning actors to those movies.
You are an Executive Producer within the company, and you are creating a system to
simplify and streamline your process.

### Description
This is Udacity's Full Stack Web Dev Nanodegree capstone project. The project
is about a Casting Agency REST API where you can access some of the following
information based on your authentication credentials:

* The **Casting Assistant** role can:
  * view actors
  * view movies
* The **Casting Director** role can:
  * All persmissions the Casting Assistant has and...
  * add an actor
  * delete an actor
  * modify an actor
  * modify a movie
* The **Executive Producer** role can:
  * All permissions the Casting Director has and...
  * Add a movie
  * delete a movie

As mentioned above, there are three roles which each has a particular set of
credentials. The RBAC (Role Based Access Control) and the
authentication side was done using [Auth0](https://auth0.com/).

The backend was built with [Python](https://www.python.org) utilizing the [Flask](https://flask.palletsprojects.com/en/2.0.x/) micro framework. The code
implementation includes basic error handling and testing with Python [unittests](https://docs.python.org/3/library/unittest.html)
(All the errors are formatted to be returned as JSON objects as well as the
endpoints). The API performs all CRUD operations and was
lauched and deployed using [Heroku](https://heroku.com). The jwt token
provided by [Auth0](https://auth0.com/) is decoded and verified in the backend.

### Tech Stack
* [Python](https://www.python.org) with [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  * Flask-Cors
  * Flask-Gunicorn
  * Flask-Migrate
  * Flask-RESTful
  * Flask-SQLAlchemy
* [PostgreSQL](https://www.postgresql.org)
* [Heroku](https://heroku.com)
* [Auth0](https://auth0.com/)

### Code Style
The backend follows all the PEP8 code style guidelines. The endpoints were planned
and structured to follow the REST arquitectural style.

## Getting Started


### Local Development
The instructions below will guide you through the process of running the
application locally on your machine.

#### Prerequisites
* The latest version of [Python](https://www.python.org/), [pip](https://pypi.org/project/pip/),
  and [PostgreSQL](https://www.postgresql.org) should already be installed on
  your machine. You can verify if you have them already on your machine by
  running the following commands:

  ```py
  # For Python:
  > python --version

  # For pip:
  > pip3 --version

  # For Node:
  > node --version

  # For PostgreSQL:
  > postgres --version
  ```
  to confirm that you have the latest version of these technologies click on
  their respective links above.


* **IMPORTANT NOTE**: The project was built with [Python 3.9.8](https://www.python.org/downloads/release/python-398/), if something doesn't work,
  just downgrade to this version of python.

* **Start a virtual environment** from the backend folder. Below are the
  instructions to do this task:
  ```py
  # Mac Users
  > python -m venv venv
  > source venv/bin/activate

  # Windows users on Git Bash. NOT CMD
  > py -m venv venv
  > venv/Scripts/activate
  ```
  If you're using the PyCharm IDE you can start a virtual environment following
  these [instructions](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env)
  from the [PyCharm official docs](https://www.jetbrains.com/help/pycharm/quick-start-guide.html)
* **Install depencies**. From the backend folder run:

  ```py
  pip3 install -r requirements.txt
  ```
### Step 1: Start/Stop the PostgreSQL server.
Mac users can follow the command below:
```
pg_ctl -D /usr/local/var/postgres start
```
if you encounter a problem, run these commands:
```
pg_ctl -D /usr/local/var/postgres stop
pg_ctl -D /usr/local/var/postgres restart
```
Windows users can follow the commands below:
* Find the database directory, it could be something like this:
`C:\Program File\PostgreSQL\13.3\data` the path depends on where you installed
postgres on your machine. If you can't find the directory, run this command:
    ```
    which postgres
    ```
    that command should output the path to where postgres is installed.
* Then, in the command line ([Git Bash](https://git-scm.com/downloads)),
execute the following command:
    ``` py
    # Start the server
    pg_ctl -D "C:\Program File\PostgreSQL\13.3\data" start
    ```
    if you encounter a problem with starting the server you can execute these
    other commands:
    ``` py
    # Stop the server
    pg_ctl -D "C:\Program File\PostgreSQL\13.3\data" stop

    # Restart the server
    pg_ctl -D "C:\Program File\PostgreSQL\13.3\data" restart
    ```
if it shows the *port already occupied* error, run:
``` py
sudo su -
ps -ef | grep postmaster | awk '{print $2}'
kill <PID>
```

### Step 2: Create and Populate the database
1. **Setup**

   In the .env file at the root folder change these variables values
   to match yours:

    ```python
    PASSWORD=<your database password>
    DATABASE_URI=postgresql://<your database username>:<your database password>@localhost:5432/casting_agency_test
    ```

2. **Create the database**

    In your terminal, navigate to the `/backend/database` directory path and run
    the following commands:

    ```py
    # Connect to PostgreSQL
    psql <your database username>

    # View all databases
    \l

    # Create the database
    \i setup.sql

    # Exit the PostgreSQL prompt
    \q
    ```

3. **Create tables**

    Once your database has been created, you can create tables and apply
    constraints

    ``` py
   # Mac & Windows users
   psql -f casting_agency.psql -U <Your database username> -d casting_agency_test

   # Linux users
   su - postgres bash -c "psql casting_agency_test < /path/to/backend/database/casting_agency.psql"
   ```

### Step 3: Start the backend server

  From the `/backend` directory run:
  ```py
  # Mac users
  export FLASK_APP=app
  export FLASK_ENV=development
  flask run

  # Windows users on CMD
  set FLASK_APP=app
  set FLASK_ENV=development
  flask run
  ```
  These commands will put the application in development mode.

  The applicatoin will run on `http://127.0.0.1:5000` by default.


#### Authentication
* In order to access most of the endpoints in the API you will need to be
authenticated with one of these three roles:
  1. Casting Assistant
  2. Casting Director
  3. Executive Producer

* You can see the endpoints they have access to at the very beginning of this
document.

* At the moment there is no way to authenticate by yourself.

* If you want to gain access to the endpoints you can email me to
[kocruz.24@gmail.com](https://gmail.com) with the subject "Casting Agency Auth Access"
and the role you want to test. I'll send you back the respective bearer token so that
you can replace it below in the API docs and gain access to the corresponding
endpoints of the role.


### Running Tests
Currently, the only way to run the tests available in this project is through
  [PyCharm](https://www.jetbrains.com/pycharm/) or some other smart IDE.
If you have already downloaded [PyCharm](https://www.jetbrains.com/pycharm/)
  then in order to run the tests do the following:

1. Find the test that you want to run under the `/tests` directory.
2. Before going to the next step, make sure you have set your 'DATABASE_URL' correctly in your .env file,
otherwise the test will fail.
3. Then in the python file, press the 'play' button circled below:

    <img src="https://res.cloudinary.com/kcruzcloud/image/upload/v1639187297/image-example-for-running-tests-in-PyCharm.png" width="600">

4. That button will run all the tests in the current python file.

If you want to run a specific test individually, you can do so by searching for
the specific function inside the python test file that you want and then following
the step #2 above.
---

## API Reference

### Getting Started
* **Base URL**: http://kcruz-casting-agency.herokuapp.com
* **Authentication**:
    If you want to gain access to the endpoints you can email me to
[kocruz.24@gmail.com](https://gmail.com) with the subject "Casting Agency Auth Access"
and the role you want to test. I'll send you back the respective bearer token so that
you can replace it below and gain access to the corresponding
endpoints of the role.

### Error Handling
Errors are returned as JSON objects in the following format:
``` py
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```

The API will return these error types when requests fail:
* `404: Resource Not Found`
* `422: Unprocessable Entity`
* `405: Method Not Allowed`
* `401: Authorization not present in headers`
* `401: header_malformed`
* `401: bearer keyword not found`
* `401: invalid_header`
* `401: token_expired`
* `400: invalid_claims`
* `403: Forbidden`
* `500: Internal Server Error`

## Endpoints

### Home Route

#### GET `/`

* General:
  * Returns a success value and home route message to confirm that
    everything is working properly.


* Sample: `curl http://kcruz-casting-agency.herokuapp.com | python -m json.tool`
* Response:
  ```json
  {
      "home_route": true,
      "success": true
  }
  ```

### Actors

#### GET `/actors`

* General:
  * Returns a list of actors, the quantity of available actors and a success
    value.


  * Sample:
    ```js
     curl -r GET \
          --url 'http://kcruz-casting-agency.herokuapp.com/actors' \
          -H 'Authorization: Bearer {token}' \
          -H 'Content-Type: application/json' | python -m json.tool
    ```


  * Response:
    ```json
    {
        "actors": [
            {
                "age": 22,
                "gender": "male",
                "id": 1,
                "name": "Kevin"
            },
            {
                "age": 21,
                "gender": "male",
                "id": 3,
                "name": "Diego"
            },
            {
                "age": 32,
                "gender": "male",
                "id": 5,
                "name": "Daniel"
            },
            {
                "age": 31,
                "gender": "male",
                "id": 6,
                "name": "Miguel"
            }
        ],
        "all_actors": 4,
        "success": true
    }
    ```

#### POST `/actors`

* General:
  * Returns a success value, the newly created actor id, and the actor object
    itself.


* Sample:
    ```js
    curl -r POST \
         --url 'http://kcruz-casting-agency.herokuapp.com/actors' \
         -H 'Authorization: Bearer {token}' \
         -H 'Content-Type: application/json' \
         -d '{
                "name": "some name",
                "age": 23,
                "gender": "other"
              }' | python -m json.tool
    ```
* Response:
    ```json
    {
        "created": 39,
        "new_actor": {
            "age": 23,
            "gender": "other",
            "id": 39,
            "name": "some name"
        },
        "success": true
    }
    ```

#### PATCH `/actors/{id}`

* General:
  * Returns an actor object before modification, the actor object after
    the modifications, and a success value.


* Sample:
    ```js
    curl --request PATCH \
         --url 'http://kcruz-casting-agency.herokuapp.com/actors/38' \
         -H 'Authorization: Bearer {token}' \
         -H 'Content-Type: application/json' \
         -d '{
                "name": "modified name",
                "age": 40,
                "gender": "female"
             }' | python -m json.tool
    ```

* Response:
    ```json
    {
        "actor_before": {
            "age": 21,
            "gender": "other",
            "id": 38,
            "name": "some name"
        },
        "modified_actor": {
            "age": 40,
            "gender": "female",
            "id": 38,
            "name": "modified name"
        },
        "success": true
    }
    ```

#### DELETE `/actors/{id}`

* General:
  * Returns the deleted actor id, the deleted actor object,
    the quantity of actors before deleting the current actor, the quantity
    after deletion, and a success value.


* Sample:
    ```js
    curl --request DELETE \
         --url 'http://kcruz-casting-agency.herokuapp.com/actors/38' \
         -H 'Authorization: Bearer {token}' \
         -H 'Content-Type: application/json' | python -m json.tool
    ```

* Response:
    ```json
    {
        "deleted_actor": {
            "age": 40,
            "gender": "female",
            "id": 38,
            "name": "modified name"
        },
        "deleted_actor_id": 38,
        "number_of_actors_after": 18,
        "number_of_actors_before": 19,
        "success": true
    }
    ```

### Movies

#### GET `/movies`

* General:
  * Returns a list of movies, the quantity of available movies and a success
    value.


* Sample:
  ```js
   curl -r GET \
        --url 'http://kcruz-casting-agency.herokuapp.com/movies' \
        -H 'Authorization: Bearer {token}' \
        -H 'Content-Type: application/json' | python -m json.tool
  ```

* Response:
    ```json
    {
        "all_movies": 4,
        "movies": [
            {
                "id": 1,
                "release_date": "Fri, 20 Oct 2006 00:00:00 GMT",
                "title": "The Prestige"
            },
            {
                "id": 7,
                "release_date": "Tue, 01 Sep 2009 00:00:00 GMT",
                "title": "Spider-Man 3"
            },
            {
                "id": 13,
                "release_date": "Sun, 07 Nov 2021 00:00:00 GMT",
                "title": "Spectre"
            },
            {
                "id": 14,
                "release_date": "Sun, 07 Nov 2021 00:00:00 GMT",
                "title": "Spectre"
            }
        ],
        "success": true
    }
    ```

#### POST `/movies`

* General:
  * Returns a success value, the newly created movie id, and the movie object
    itself.


* Sample:
    ```js
    curl -r POST \
         --url 'http://kcruz-casting-agency.herokuapp.com/movies' \
         -H 'Authorization: Bearer {token}' \
         -H 'Content-Type: application/json' \
         -d '{
                 "title": "some movie title",
                 "release_date": "2024-12-23"
             }' | python -m json.tool
    ```

* Response:
    ```json
    {
        "created_id": 15,
        "new_movie": {
            "id": 15,
            "release_date": "Mon, 23 Dec 2024 00:00:00 GMT",
            "title": "some movie title"
        },
        "success": true
    }
    ```

#### PATCH `/movies/{id}`

* General:
  * Returns an movie object before modification, the movie object after
    the modifications, and a success value.


* Sample:
    ```js
    curl --request PATCH \
         --url 'http://kcruz-casting-agency.herokuapp.com/movies/15' \
         -H 'Authorization: Bearer {token}' \
         -H 'Content-Type: application/json' \
         -d '{
                 "title": "modified movie name"
             }' | python -m json.tool
    ```

* Response:
    ```json
    {
        "modified_movie": {
            "id": 15,
            "release_date": "Mon, 23 Dec 2024 00:00:00 GMT",
            "title": "modified movie name"
        },
        "old_movie": {
            "id": 15,
            "release_date": "Mon, 23 Dec 2024 00:00:00 GMT",
            "title": "some movie title"
        },
        "success": true
    }
    ```

#### DELETE `/movies/{id}`

* General:
  * Returns the deleted actor id, the deleted movie object,
    the quantity of movies before deleting the current movie, the quantity
    after deletion, and a success value.


* Sample:
  ```js
  curl --request DELETE \
       --url 'http://kcruz-casting-agency.herokuapp.com/movies/15' \
       -H 'Authorization: Bearer {token}' \
       -H 'Content-Type: application/json' | python -m json.tool
  ```

* Response:
  ```json
  {
      "deleted_movie": {
          "id": 15,
          "release_date": "Mon, 23 Dec 2024 00:00:00 GMT",
          "title": "modified movie name"
      },
      "number_of_movies_after": 4,
      "number_of_movies_before": 5,
      "success": true
  }
  ```