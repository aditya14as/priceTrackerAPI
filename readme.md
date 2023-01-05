# Django Rest API for fetching realtime price of Bitcoin and storing it in database

## API End Points
* User Registration (http://127.0.0.1:8000/users/register)
* User Login (http://127.0.0.1:8000/users/login)
* Fetching realtime price of Bitcoin and saving it to the database (http://127.0.0.1:8000/price/fetch_price)
* Showing all the list of price with timestamp and pagination (http://127.0.0.1:8000/price/list_price?page=2)

## Step-1 Clone

```sh
$ git clone https://github.com/aditya14as/priceTrackerAPI.git
$ cd priceTrackerAPI
```

## Step-2 Create a virtual environment:

```sh
$ pip install pipenv
$ pipenv shell
```

## Step-3 Install  all the dependencies:

```sh
$ pipenv install -r requirements.txt
```

## Step-4 After successfull installation of the dependencies:
```sh
$ python manage.py runserver
```



