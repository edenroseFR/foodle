from app.models.donor import Donor
from app.models.collector import Collector
from flask import session
import datetime
from werkzeug.datastructures import FileStorage
import cloudinary.uploader as cloud

def show_donor_details(session_email):
    donor = Donor()
    return donor.get_donor_details(session_email)

def get_total_foods(session_email):
    total_kilos = 0
    donor= Donor()
    kilos = donor.donation_stat_foods(session_email)
    for item in kilos:
        total_kilos += item[0]

    return total_kilos

def get_total_beverages(session_email):
    total_liters = 0
    donor= Donor()
    liters = donor.donation_stat_beverages(session_email)
    for item in liters:
        total_liters += item[0]

    return total_liters

def get_total_food_distributed(session_email):
    total_kilos = 0
    donor= Donor()
    kilos = donor.donation_stat_food_distributed(session_email)
    for item in kilos:
        total_kilos += item[0]

    return total_kilos

def get_total_bev_distributed(session_email):
    total_liters = 0
    donor= Donor()
    liters = donor.donation_stat_bev_distributed(session_email)
    for item in liters:
        total_liters += item[0]

    return total_liters


# for collector's dashboard
def get_organization_donors(session_email):
    collector_id = Collector().get_id(session_email)
    donors = Collector().get_donors(collector_id)
    return donors

   
def get_items_for_distribution(session_email):
    collector_id = Collector().get_id(session_email)
    items_for_distribution = Collector().get_to_distribute(collector_id)
    return items_for_distribution

def set_distributed_to_true(donation_id):
    Collector().set_distribute_to_true(donation_id)
    return None


def get_items_to_collect(session_email):
    collector_id = Collector().get_id(session_email)
    items_to_collect = Collector().get_items_to_collect(collector_id)
    return items_to_collect


def set_collected_to_true(donation_id):
    collector_id = Collector().get_id(session['email_address'])
    date_collected = datetime.datetime.now()
    Collector().set_collected_to_true(donation_id, collector_id, date_collected)
    return None

def get_collectors(email_address):
    collectors = Donor().get_collectors(email_address)
    return collectors

#
def get_collector_id():
    collector_id = Collector().get_id(session['email_address'])

    return collector_id

    return None
def get_completed_collections(email_address):
    collector_id = Collector().get_id(email_address)
    completed = Collector().get_completed_collections(collector_id)
    return completed

def get_image_url(file: FileStorage):
    upload_image = cloud.upload(file)
    url = upload_image.get('url')
    return url

def save_distribution_images(donation_id: int, images):
    Collector().save_distribution_images(donation_id, images)
    return None

def record_distribution(donation_id: int) -> None:
    collector_id = Collector().get_id(session['email_address'])
    time_created = datetime.datetime.now()
    Collector().record_distribution(donation_id, collector_id, time_created)

def set_collected_to_false(donation_id):
    collector_id = Collector().get_id(session['email_address'])
    date_collected = datetime.datetime.now()
    Collector().set_collected_to_false(donation_id)
    return None

def get_total_food_bev_distributed(email_address):
    total_distribution = Collector().get_total_food_bev_distributed(email_address)
    return total_distribution
