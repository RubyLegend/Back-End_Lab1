# Back-End Lab 1

> Made by Serhii Hatsan, IK-01
--------------------------------------------------------

## Warning
```
Do not try to use it on production server, or anywhere except of your own machine.
I won't be responsible for any damage, that will be caused by this code 
(broken server, nuclear war, computer overheating...).
```

--------------------------------------------------------

## Determining variant
- Group: IK-01
- 1 % 3 = 1

So, my own task is: "Валюти".

## Available endpoints
- / - main page
- /users (GET, POST, DELETE) - actions with users
- /categories (GET, POST, DELETE) - actions with categories
- /records (GET, POST) - actions with records
- /currencies (GET, POST, DELETE) - actions with currencies
- /swagger-ui - self-documented code

## How to run it locally
1. Install [docker](https://www.docker.com/)
2. Install [docker compose](https://github.com/docker/compose)
3. Run ```docker compose build```
4. Run ```docker compose up```

Now you can send POST and GET request to your server, which is serving on ```127.0.0.1:80```.

- If you need to change port, on which server will be opened, navigate to ```docker-compose.yaml``` and change value for ```PORT``` variable.

## How to test it with Postman
1. Install [Postman](https://www.postman.com)
2. Import Postman collection ```File - Import - 'Select file' - 'Import'```
3. Change values
4. Run tests