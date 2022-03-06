import cloudinary.uploader as cloud
from werkzeug.datastructures import FileStorage
from app.models.donation import Donation
from app.models.donor import Donor


donation = Donation()


def get_image_url(file: FileStorage):
    upload_image = cloud.upload(file)
    url = upload_image.get("url")
    return url


def category_options():
    options = donation.get_category_options()
    return options


def transport_mode_options():
    options = donation.get_tmode_options()
    return options


def show_donor_details(session_email):
    donor_details = Donor().get_donor_details(session_email)
    return donor_details


def show_donation_items(donation_id):
    donation_items = Donation.show_donation_items(donation_id)
    return donation_items


def add_donation(
    email_address, added_items, datetime, transport_mode, street, barangay, city
):
    Donation().add_donation(
        email_address,
        added_items,
        datetime,
        transport_mode,
        street,
        barangay,
        city,
    )


def get_donation_details(donation_id):
    details = Donation.get_donation_details(donation_id)
    return details


def update_donation_util(
    donation_id,
    update_donation_added_items,
    datetime,
    transport_mode,
    number_of_items,
    street,
    barangay,
    city,
):
    donation = Donation()
    donation.update_donation(
        donation_id,
        update_donation_added_items,
        datetime,
        transport_mode,
        number_of_items,
        street,
        barangay,
        city,
    )
