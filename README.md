<img src="logo2.jpg">

# meeting-scheduler
A web application for scheduling meeting. In the current digitized world and in the midst of 
Covid-19 pandemic, the daily activities like meetings moved from physical to online or even blended.
To have it all planned therefore, a digital solution therefore is inevitible and at this point comes 
the meeting scheduler.

## How to run it
This web application is developed in django and Fauna. Faunadb usually runs on FQL and also GraphQL.
To run the project therefore, install django and faunadb.
The secret key is already in place, as this is just a prototype, the main application will run on 
postgres in production.

# Acquire the project from github
git clone git@github.com:joseph-njogu/meeting-scheduler.git (For the ssh)
git clone https://github.com/joseph-njogu/meeting-scheduler.git (For the https)

### Create a virtual environment
python3 -m venv venv
then
### Activate the virtual environment
source venv/bin/activate
or
. venv/bin/activate
## Install the project dependencies as listed in the requirements file
pip3 install -r requirements.txt

Once the requirements are installed, navigate to the root of the project, where manage.py file is located.
# From here:
### Setup the database through making migrations.
python3 manage.py makemigrations
python3 manage.py migrate

After a successful migration of the database,
### Start the server
python3 manage.py runserver

That's all, you can now access the web application via your favourite browser, using the link provided after a successful running of the server.
