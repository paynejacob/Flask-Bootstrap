# points-tracker
An simple web app for tracking arbitrary points

# Dev Environment
# requires bower command
npm install -g bower-cli
# virtualenv reccomended
# requires postgres and user (see settings)
brew install postgres
# actual setup
export APP_ENV="dev"
pip install -r requirements.txt
bower install
python manage.py create_db
python manage.py db upgrade
python manage.py create_user
python manage.py server
