# Bond store

## Run docker compose

Documentation [Docker compose](https://docs.docker.com/samples/django/) to use with django


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


To see the swagger documentation about endpoints, run [Local Documentation](http://localhost:8000/swagger/)

###Curls examples


Create user
```bash
curl --location --request POST 'http://localhost:8000/api/users/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "pablo@gmail.com",
    "password": "1234",
    "username": "pablo"
}'
```

login
```bash
curl --location --request POST 'http://localhost:8000/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "pablo@gmail.com",
    "password": "1234"
}'
```
get bonds MXN

```bash
curl --location --request GET 'http://localhost:8000/api/bonds/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMjk5MDMzLCJqdGkiOiIyMzIzYTg0ZjY3NGQ0MmQxYjk0MWI3YzVkYWVkN2FiZSIsInVzZXJfaWQiOjJ9.PP1_wYnBggd6jnHVFVmhPQA0lUD6S7PtiqshnFJbDsg'
```

get bonds UDS

```bash
curl --location --request GET 'http://localhost:8000/api/bonds/usd' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMzA2NjE5LCJqdGkiOiI5YzBlN2M1ZmViYTg0ZjRmOTU4ZGI2MWIxMjQ2NDFhYiIsInVzZXJfaWQiOjJ9.JZA8gaVygwHmogn_A276k-VfDwwGLh5L0Zh6knb3Prg'
```

sell one bond
```bash
curl --location --request POST 'http://localhost:8000/api/sell_bonds/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMjk5MDMzLCJqdGkiOiIyMzIzYTg0ZjY3NGQ0MmQxYjk0MWI3YzVkYWVkN2FiZSIsInVzZXJfaWQiOjJ9.PP1_wYnBggd6jnHVFVmhPQA0lUD6S7PtiqshnFJbDsg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type":"123456789asdf",
    "total_sell": 99,
    "price_total":"9,999.9999"
}'
```

sell many bonds
```bash
curl --location --request POST 'http://localhost:8000/api/sell_bonds/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMjk5MDMzLCJqdGkiOiIyMzIzYTg0ZjY3NGQ0MmQxYjk0MWI3YzVkYWVkN2FiZSIsInVzZXJfaWQiOjJ9.PP1_wYnBggd6jnHVFVmhPQA0lUD6S7PtiqshnFJbDsg' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "type":"123456789asdf",
        "total_sell": 99,
        "price_total":"9,999.9999"
    },
    {
        "type":"123456789asdf",
        "total_sell": 100,
        "price_total":"109,999.9999"
    }
]'
```
buy bond

```bash
curl --location --request POST 'http://localhost:8000/api/buy_bonds/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMjk5MDMzLCJqdGkiOiIyMzIzYTg0ZjY3NGQ0MmQxYjk0MWI3YzVkYWVkN2FiZSIsInVzZXJfaWQiOjJ9.PP1_wYnBggd6jnHVFVmhPQA0lUD6S7PtiqshnFJbDsg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bond_id":1
}'
```


## Considerations

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
- Create_id and buyer_id are foreign keys to users
- When creating a bond, internally it relates the user to creator_id


## user_api
- To authenticate, the JWT library was used, with email and password.
- You need to loggin to use the api, with the exception
/api/tokens/ and /api/refesh


## banxico_externalapi
- As the USD Exchange rate varies only from Monday to Friday, and on Saturdays and Sunday does not has new values, for this model it was decided take as a refer the last Friday USD Exchange rate.
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
## CLIENT REQUERIMENTS CHECKLIST
### SELL
- Can the user sell publish one or more bonds per sale? 👍, LIST ARE USED

- Each item published include: 
    - Name of type of bond as a string with a mínimum of 3 and máximum of 40 alphanumeric chars? 👍
    - Number of bond for sale as a integer with an inclusive range of 1 to 10,000? 👍
    - Selling Price of the total number of bonds for sales, as a monetary value with an inclusive range of 0.0000 to 100,000,000.0000 and a resolution of four decimal numbers? 👍
    The number is received in the format 100,000,000.0000 but it is saved as a decimal to facilitate operations.
        - The selling Price it is represented in Mexican Pesos (MXN)?  👍
- Does the API respond with an error when a user publishes ítems that do not comply with the parameters described aboved? 👍
- Does the system assign a unique ID for each publication? 👍
- Does the system assign a unique ID for each publication and link it to the user that submits it? 👍

### BUY
- Is the user able to list the published ítems and buy them trough a unique ID? 👍, BOND BY BOND 
- Is a published item considered “purchased” if they always have a buyer linked to it? 👍
- Does the API throw an error indicating that the operation is invalid if a buyer tries to buy an item that has already been bought? 👍 
- Does the buyer have an option to list the published ítems in USD dollars using the most recent exchage rate published by Banco de Mexico? 👍 A model was added to save the exchange value of the peso against the dollar, to avoid constant requests to the external api.

### ADITIONAL REQUERIMENTS
- Does the API implement an authentication? 👍, BY JWT with duration of 1 hour per token.
- Are only authenticated users able to make API calls? 👍, EXCEPT TO CREATE A NEW USER AND TO AUTHENTICATE. 
- Does the API have a rate of 1000 calls/ min? 👍 [the following documentation was used](https://www.django-rest-framework.org/api-guide/throttling/#throttling) , EXCEPT FOR THE AUTHENTICATION METHODS.
- If you have experience with unit test, did you add your code? 👍
- If you have experience with Docker, did you create a container in wich the system runs? 👍
- Did you add a Dockerfile and usage instructions to the repository? 👍
- Did you include documentation that indicates how the project should be launched and how the API calls should be made? 👍
- Did you describe the main considerations you take during the development of your solution? 👍
- Can the solution be run locally? 👍
- Does it allow interaction trough a terminal trough http calls, or trough an interactive API explorer? 👍
    


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.