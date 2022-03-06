from flask import Blueprint

collectors_view_bp = Blueprint('collectors_view', __name__)

from . import routes