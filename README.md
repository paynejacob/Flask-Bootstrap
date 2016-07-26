# Flask App Bootstrap
An simple Flask app Template with:
* User Authentication
* Notifications
* Webpack + ES2015 + Bootstrap Frontend
* Asset Management
* Sass Styles

# First Time Setup

```
pip install -r requirements.txt
./manage.py npm_update
./manage.py db upgrade
./manage.py create_user
```

#Starting the development Server
### Set the environmental variables

```
export APP_ENV="dev"
```
### Start the server
```
./manage.py runserver
```

# Database migrations
```
./manage.py db migrate
./manage.py db upgrade
```
