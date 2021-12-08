# Casting Agency

---

### Description
This is Udacity's Full Stack Web Dev Nanodegree capstone project. The project
is about a Casting Agency API where you can access some of the following 
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

The backend was built with Python utilizing the Flask micro framework. The code
implementation includes basic error handling and testing with Python unittests 
(All the errors are formatted to be returned as JSON objects as well as the
endpoints). The API performs all CRUD operations and the jwt token
provided by [Auth0](https://auth0.com/) is decoded and verified in the backend.

### Code Style
The backend follows all the PEP8 code style guidelines. The endpoints were planned
and structured to follow the REST arquitectural style.

## Getting Started

---

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
  > pip --version
  
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
  pip install -r requirements.txt
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
  
    In your terminal, naviate to the `/backend/database` directory path and run
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

  From the root directory run:
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
* Upcoming...

























