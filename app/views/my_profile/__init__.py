from flask import Blueprint

my_profile_bp = Blueprint('my_profile', __name__)

from . import routes