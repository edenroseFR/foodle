from app.models.donor import Donor
from app.models.collector import Collector
from flask import session
import datetime
from werkzeug.datastructures import FileStorage
import cloudinary.uploader as cloud

def show_donor_details(session_email):
    donor = Donor()
    return donor.get_donor_details(session_email)

def get_total_food_bev_distributed(email_address):
    total_distribution = Collector().get_total_food_bev_distributed(email_address)
    return total_distribution

def get_organization_donors(session_email):
    collector_id = Collector().get_id(session_email)
    donors = Collector().get_donors(collector_id)
    return donors