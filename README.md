# Food Donation Web Application

## FEATURES

- Post, Track, Manage

## SETUP & INSTALLATION

1. Clone the repository to your local machine by running the following command on your command-line.

```bash
clone https://github.com/edenroseFR/foodle.git
```
2. Navigate inside the foodle folder

```bash
cd foodle
```
3. Create a virtual environment

```bash
virtualenv venv
```
4. Activate the virtual environment

```bash
cd venv/Scripts/activate
```
5. Install all the requirements.

```bash
pip install -r requirements.txt
```
6. Create a dotenv file.

```bash
type nul > .env
```
7. Open the .env file and write the following:

```python
SECRET_KEY = value

DB_HOST= value
DB_NAME= fododb
DB_USERNAME= value
DB_PASSWORD= value

CLOUD_NAME = value
API_KEY = value
API_SECRET = value
PHOTO_UPLOAD = cloud
```
8. Create a flaskenv file.

```bash
type nul > .flaskenv
```
9. Open the .flaskenv file and make sure it contains the following:

```python
FLASK_APP=foodle
FLASK_ENV=development
FLASK_RUN_PORT=8080
```
10. In your MySQL IDE, execute the script.sql file located in `foodle/database_script`

## RUNNING THE APP

1. Activate the virtual environment

```bash
cd venv/Scripts/activate
```
2. Run

```bash
flask run
```
