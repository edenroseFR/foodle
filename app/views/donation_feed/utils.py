from app.models.donor import Donor  # absolute imports
from app.models.donation import Donation


def show_donor_details(session_email):
    donor_details = Donor().get_donor_details(session_email)
    return donor_details


def get_donor_id(session_email):
    donor_id = Donor().get_donor_id(session_email)
    return donor_id


def get_posted_donations(session_email, role="donor"):
    donor_id = get_donor_id(session_email)
    posted_donations = Donation().get_posted_donations(donor_id, role)
    return posted_donations


def get_reserved_donations(session_email):
    donor_id = get_donor_id(session_email)
    reserved_donations = Donation().get_reserved_donations(donor_id)
    return reserved_donations


def get_collected_donations(session_email):
    donor_id = get_donor_id(session_email)
    collected_donations = Donation().get_collected_donations(donor_id)
    return collected_donations


def get_distributed_donations(session_email):
    donor_id = get_donor_id(session_email)
    distributed_donations = Donation().get_distributed_donations(donor_id)
    return distributed_donations


def delete_donation(donation_id):
    Donor().delete_donation(donation_id)
    return None


def cancel_reserved_donation(donation_id, is_delete):
    Donation().cancel_reserved_donation(donation_id, is_delete)
    return None


def get_collected_donation_details(session_email):
    donor_id = get_donor_id(session_email)
    details = Donation().get_collected_donation_details(donor_id)
    return details


def get_distributed_donation_details(session_email):
    donor_id = get_donor_id(session_email)
    details = Donation().get_distributed_donation_details(donor_id)
    return details


def get_distributed_donation_photo(session_email):
    donor_id = get_donor_id(session_email)
    photos = Donation().get_distributed_donation_photo(donor_id)
    return photos
