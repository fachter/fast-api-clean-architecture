# fast-api-clean-architecture
A REST Api template for python with FastApi, MongoDB and JWT authentication in clean architecture


# References

The example is following fastapi docs. Check it out to learn more about it: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


# Setup

## Database
First install docker and docker-compose (or use any other way to set up a mongodb instance)

Create a '.env' file similar to '.env.local'
You can create a new SECRET_KEY with following command in the terminal
```shell
openssl rand -hex 32
```

With the next command you can start the docker container with the mongodb
```shell
docker-compose up
```
It will use the values from the '.env' file as username and password

In [database.py](app/repositories/database.py) you can change additional configuration if you are using a different host or port for example.

If you want to use anything else than MongoDB, change the implementation of the repositories ([user_repositories](app/repositories/user_repository.py) and [database](app/repositories/database.py))


## Python

The following command will install all the required dependencies listed in [Pipfile](Pipfile), like fastAPI and pymongo
```shell
pipenv install
```

Start the server by running
```shell
cd app
```
```shell
uvicorn app:app --reload
```

The first 'app' relates to the folder where are the source code is located.

The second 'app' relates to the file name [app.py](app/app.py)

The third 'app' has to be the same name as the variable inside the file, which holds an instance of FastApi(), like in the following
```python
from fastapi import FastAPI
app = FastAPI()
```

More information can be read in the official docs: https://fastapi.tiangolo.com/tutorial/first-steps/


# Usage

After completing the previous steps, there should now be a server running on http://127.0.0.1:8000/

In order to see all possible urls, go to http://127.0.0.1:8000/docs/

Some of the routes require authentication, for which a new user needs to be entered into the db with a post request to http://127.0.0.1:8000/users/add 


# Structure

- routers: Urls can be grouped into routers (also known as controllers)
- usecases: From there use cases are called
- repositories: The use cases are communicating with the database through repositories located in the package with the same name 
- documents: Inside the documents package, classes (also known as entities when using a relational db) that are used for storing data in mongodb are located. 
- viewmodel: This package contains models that are presented to or send by the user.
- config: Here any file that stores configuration of the app is located, like some security functions

