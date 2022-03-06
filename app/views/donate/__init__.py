from flask import Blueprint

donate_bp = Blueprint("donate", __name__)

from . import routes
