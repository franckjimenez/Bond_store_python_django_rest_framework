
# Bond store

Foobar is a Python library for dealing with word pluralization.

## Run docker compose

Documentation [Dockercompose](https://docs.docker.com/samples/django/) to use with django


To run the program you should be on the /demo/ path and run the following command in the console

```bash
docker-compose up
```

The service will be available in http://localhost:8000/

## Configuration

```
Database: 
- postgres
Python:
- Django>=3.0,<4.0
- psycopg2-binary>=2.8
- djangorestframework == 3.12.0
- djangorestframework-simplejwt==4.8.0
- requests==2.26.0
- drf-yasg
```



## Documentation
To see the swagger documentation about endpoints, run [LocalDocumentation](http://localhost:8000/swagger/)

## Consideration

### Generated models
```
bond_api
- id
- type
- total_sell
- price_total
- create_id
- buyer_id

user_api
- id
- email
- username
- password

banxico_externalapi
- id
- last_date 
- dollar_price
```
## bond_api
- All users can buy and sell bond if they are logged in
- Regular expressions were made to validate the data when they enter the system
- In the case of price_total, it was decided to save the data as decimals and not as a string to facilitate future operations.
- create_id and buyer_id are foreign keys to users
- When creating a bond, internally it relates the user to creator_id


## user_api
- To authenticate, the JWT library was used, with email and password.
- You need to loggin to use the api, with the exception
/api/tokens/ and /api/refesh


## banxico_externalapi
- For this model it was decided to save the data since they do not vary constantly but the values ​​are per day, the data was also analyzed
and the update of them is only from Monday to Friday, taking Friday as a reference for weekends
- A logic was added to handle the date and reduce the number of requests to the external api.

## Running the tests ⚙️
```bash
python manage.py test
```
### Unit test

```bash
- login
- user creation
- get bond list MNX
- get bond list USD
- create one bond to sell
- create many bond to sell
- buy a bond
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

