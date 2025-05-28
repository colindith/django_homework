# django_homework

## Quick Start

1. Clone the repo from github
```
git clone https://github.com/colindith/django_homework.git
cd django_homework
```
2. Run the server with docker-compose. This cmd would occupy a cmd line tab. Open a new tab to continue.
```commandline
docker-compose up
```
3. Create a superuser, so that you can log in to the admin.
```commandline
docker-compose run app python manage.py createsuperuser
```
4. Open the browser. Enter into the login page and admin page.
```
http://127.0.0.1:8000/       # user login page
http://127.0.0.1:8000/admin/ # admin page
```
You may create a new user in admin or use the superuser account to login.
## Unit Test
To run the unit test, you might want to fix the Python in a proper version. A convenient way to do so is to use uv. Here we assume that the uv tool is already being in your system. So we can skip the installment part.
This command shows all the available python version in your computer.
```commandline
uv python list
```
Use uv to create a new virtual environment in the root directory of the repository.
```commandline
 uv venv --python 3.11
```
And install all the packages.
```commandline
uv pip install -r requirements.txt
```
Now you can activate the virtual environment we just created.
```commandline
# Linux / macOS
source .venv\Scripts\activate

# Windows
.venv\Scripts\activate.bat
```
Then run the unit test under `securities` directory.
```commandline
cd securities
python manage.py test
```
