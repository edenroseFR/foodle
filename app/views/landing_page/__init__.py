from flask import Blueprint

landing_bp = Blueprint('landing',__name__)

from . import routes