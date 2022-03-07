# food Donation Web Application

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
DB_HOST=your_database_host
DB_NAME=fododb
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
SECRET_KEY=any_string_will_do

CLOUD_NAME = your_cloudinary_name
API_KEY = your_cloudinary_api_key
API_SECRET = your_cloudinary_api_secretkey
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
