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
```

Install npm and Node JS:

```
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm
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

## Running the tests

Currently no tests are created for this system

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Python
Django
Jquery

## Contributing

Left blank

## Versioning

Left blank

## Authors

Joe Brotzer
Ethan Mosqueda
Rendave Lecciones

## License

Left blank

## Acknowledgments

* Thanks to Peter for helping us with this code and helping us correct mistakes
