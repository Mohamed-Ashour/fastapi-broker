# fastapi-broker

A simulation for stocks broker that receive stream of stocks, store them and make them available for purchase using fastapi framework, vernemq queue and postgres db. 

## getting started

Start docker services

`docker-compose up -d`

The api will be running on

`localhost:8000`

The swagger docs

`localhost:8000/docs`

pg admin
`localhost:5050`

user: pgadmin4@pgadmin.org
password: admin
