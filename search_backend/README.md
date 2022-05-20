# Development
## Install requirements
```
pip install -r requirements.txt
```

## Run local development server

```
set FLASK_APP=server.py
set FLASK_ENV=development
set elastic_read_username="backend_username"
set elastic_read_password="backend_password"
flask run
```


# Docker
## Build docker image
In the root folder (where the config.yaml file is) run:
docker build -t search_backend:latest -f ./search_backend/Dockerfile .

## Run docker container
```
docker run --name search_backend --net <the network name of elasticsearch docker> <environment variables> search_backend:latest
-e elastic_admin_username=<elastic admin username>
-e elastic_admin_password=<elastic admin password>
-e elastic_write_username=<crawler user username>
-e elastic_write_password=<crawler user password>
-e elastic_read_username=<backend user username>
-e elastic_read_password=<backend user password>
```

# Start 
  docker start search_backend

# REST API
## HTTP GET /ping
Ping connection: 200 OK / 500 Connection failed

## HTTP POST /search
Basic search with the given term

# CONFIGURATIONS
Configurations are in the parent folder config.yaml with default configurations. Explanations below:

elasticsearch
   host - the address where the elastic runs on
   port - the port where the elastic runs on
   indexname - the index name the backend uses for searching
   index_reader_rolename - the backend user role (ALLOW ONLY PING AND READING THE INDEX)


# SET UP
Setting up script (./src/setup.py) contains logic for
* creating the users and roles
* creating the indexes with the analyzers and other settings

Starting the docker will run the setup script and then start the server.
If the users, roles and indices already exists, setup script will exit and the server is started.


Manual steps for creating the role and the user
1. Log into kibana
2. Go to Stack management -> Roles
3. Create a new role
   1. Name: <rolename>
   2. Cluster privileges: cluster:monitor/main (otherwise the ping request will fail - what else does this allow??)
   3. Indices: <my-indice-prefix>*
   4. Privileges: read
4. Go to Stack management -> Users
5. Create user
   1. Name: <username>
   2. Roles: <rolename>