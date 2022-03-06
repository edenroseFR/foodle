from flask import Blueprint

donation_feed_bp = Blueprint("donation_feed", __name__)

from . import routes
