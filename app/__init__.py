from flask import Flask, blueprints
from config import SECRET_KEY, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST
    )

    from app.views.login import login_bp
    app.register_blueprint(login_bp)