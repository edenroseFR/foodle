# Food Donation Web Application

## FEATURES

- Post, Track, Manage

## SETUP & INSTALLATION

1. Clone the repository to your local machine by running the following command on your command-line.

```bash
clone https://github.com/edenroseFR/foodle.git
```

2. Install all the requirements.

```bash
pip install -r requirements.txt
```

3. Create a dotenv file.

```bash
type nul > .env
```

4. Open the .env file and write the following:

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

5. Create a flaskenv file.

```bash
type nul > .flaskenv
```

6. Open the .flaskenv file and make sure it contains the following:

```python
FLASK_APP=foodle
FLASK_ENV=development
FLASK_RUN_PORT=8080
```

7. In your MySQL IDE, execute the script.sql file located in `foodle/database_script`

## RUNNING THE APP

1. Activate the virtual environment

```bash
cd venv/Scripts/activate
```

2. Run

```bash
flask run
```
