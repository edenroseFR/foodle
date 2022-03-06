from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash
from ...models.user import User
from ...models.donor import Donor
import cloudinary.uploader as cloud
import base64
from flask import session


def get_user_data(type: str, email: str) -> list:
    all_info = User().get_user(email)
    if type == "personal":
        user_data = all_info[:5]
    elif type == "address":
        user_data = all_info[5:8]
    elif type == "password":
        user_data = all_info[8]
    elif type == "privacy":
        user_data = all_info[9:11]
    elif type == "organization":
        user_data = all_info[11:13]
    elif type == "notifications":
        user_data = all_info[-1]
    return user_data


def get_user_image(email: str) -> str:
    user_data = User().get_user(email)
    image = user_data[0]
    return image


def get_role(email: str) -> str:
    role = User().get_role(email)
    return role


def has_org(email: str) -> bool:
    org = User().check_org(email)
    if org:
        return True
    return False


def hash_password(password: str = None) -> str:
    hashed_password = generate_password_hash(password, "pbkdf2:sha256", salt_length=16)
    return hashed_password


def save_changes(user: str, new_data: list, section: str) -> None:
    if section == "personal":
        User.update_personal_info(user, new_data)
        return
    if section == "address":
        User.update_address_info(user, new_data)
    elif section == "organization":
        User.update_org_info(user, new_data)
        return
    elif section == "password":
        new_data[0] = generate_password_hash(new_data[0])
        User.update_password(user, new_data)
        return
    elif section == "privacy":
        for data in range(len(new_data)):
            if new_data[data] == "on":
                new_data[data] = 1
            else:
                new_data[data] = 0
        User.update_privacy(user, new_data)
        return
    elif section == "notifications":
        if new_data[0] == "on":
            new_data[0] = 1
        else:
            new_data[0] = 0
        User.update_notifications(user, new_data)
        return


def get_image_url(file: FileStorage):
    upload_image = cloud.upload(file)
    url = upload_image.get("url")
    return url


def delete_image(link: str) -> None:
    file_name = (link.split("/")[-1]).split(".")[0]
    cloud.destroy(file_name)
    return


def check_password_match(password: str, user: str) -> bool:
    match = User().check_password_match(user, password)
    if match:
        return True
    return False


def show_donor_details(session_email):
    return Donor().get_donor_details(session_email)


def parent_orgs():
    donor_details = Donor.get_donor_details(session["email_address"])

    parents = Donor.get_parent_orgs(donor_details["user_id"])

    return parents

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

def get_collectors(email_address):
    collectors = Donor().get_collectors(email_address)
    return collectors