# Channelfix-Internship

A convenient multi-cast streaming application.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

What things you need to install the software and how to install them

```
Python version 3.0 or later
Django version 2.0 or later
```

### Installing

Create a virtual environment by follwing this guide: http://virtualenvwrapper.readthedocs.io/en/latest/install.html
Then install the prequisites using:

```
pip install django
pip install social-auth-app-django
pip install django-sslserver
pip install celery
pip install django-celery-beat
sudo apt-get install rabbitmq-server
```

Install npm and Node JS:

```
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm
```

Install Opentok:

```
sudo npm install opentok --save
```

Install Gulp:

```
sudo npm install -g gulp
```

Then get the project files from the repository by using:

```
git clone https://github.com/ethanray123/Channelfix-Internship.git
```

Note: You need to install git to use this command but is not required for the project as a whole.
Once cloned, move to the project directory:

```
cd Channelfix-Internship
```

In the project folder, install Semantic UI:

```
sudo npm install semantic-ui --save
```

Select the Automatic Set-up for Semantic UI using the arrow keys and press Enter.
Confirm that you are in the project folder.
You will be then prompted on where to install the semantic folder. Enter the following directory:

```
stream/static/semantic/
```

cd into semantic directory and build using gulp:

```
cd stream/static/semantic
gulp build
```

## Running the application

To run the application, start by running the RabbitMQ server:
```
systemctl start rabbitmq-server
```

Check the status of the RabbitMQ server with:
```
systemctl start rabbitmq-server
```

You should see `active` on your console if it is running.
Next run the celery task on a seperate console using:
```
celery -A projectname worker -B
```

Once that is running, run the django ssl server using: 
```
python manage.py runsslserver localhost:8000
```
Just replace the url with something you are using.

And that's it, simply access the url and you should be able to run the application.

## Built With

Python
Django
Jquery

## Authors

Joe Brotzer
Ethan Mosqueda
Rendave Lecciones

## Acknowledgments

* Thanks to Peter for helping us with this code and helping us correct mistakes
