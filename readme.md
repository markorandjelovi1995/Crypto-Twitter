## Install python

Go to https://www.python.org/ to install the latest version of python for your OS

For Windows : https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe

For MacOS : https://www.python.org/ftp/python/3.9.6/python-3.9.6-macosx10.9.pkg

For Linux:

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

wget -O https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tar.xz

tar -xf Python-3.9.6.tar.xz

./configure --enable-optimizations

make -j 4

sudo make altinstall

## Setup

installing dependencie
```sh
pip3 install pipenv
```
Go inside the project folder after that type the following command
```sh
pipenv install
pipenv shell
```

# Running the program

To populate the sql database
```sh
python3 twitter_scraper.py
```
To run the web app locally
```sh
python3 manage.py runserver
```

Visit http://127.0.0.1:8000/