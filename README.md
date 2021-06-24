## Starnavi Test task: python developer

This is a test task for python developer built with Django, DRF. API has basic models as User, Post and Reaction.

### API has following features:
* User signup
* User login via jwt token
* Post creation
* Like Post
* Unlike Post
* Analytics about amount of likes aggregated by day
* User activity analytics

### JWT token was implemented as another django app

### Running
```bash
# install dependencies
$ pip install -r requirements.txt

# migrate database
$ python manage.py makemigrations
$ python manage.py migrate

# start serving on 8000 port
$ python manage.py runserver
```

### Testing
```bash
# start tests
$ python manage.py test
```

### API documentation
For API documentation **Swagger** was used
> At 127.0.0.1:8000/docs/

