from ...models.user import User
from ...models.role import Role
from werkzeug.security import generate_password_hash
import random
import string
import smtplib
from email.message import EmailMessage
from os import getenv

def user_found(email: str = None, password: str = None) -> bool:
    user_exist = User().check_credentials(email, password)
    if user_exist == True:
        return True


def hash_password(password: str = None) -> str:
    hashed_password = generate_password_hash(password, 'sha256')
    return hashed_password


def get_role_id(role: str = None) -> int:
    role_id = Role.get_id(role)
    return role_id


def random_characters():
    char_count = 10
    random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k = char_count))
    return random_char


def gmail_code(code: str = None, reciever: str = None) -> None:
    msg = EmailMessage()
    msg['Subject'] = 'FODO Reset Code'
    msg['From'] = 'Food Donation'
    msg['To'] = reciever
    content = f'Your reset code: {code}'
    msg.set_content(content)


    # Establish connection
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(getenv('FODO_GMAIL_ADDRESS'), getenv('FODO_GMAIL_PASSWORD'))

    # Send mail
    server.send_message(msg)
    return None


def check_email_registration(email):
    email_exist = User().check_email_existence(email)
    if email_exist:
        return True
    return False


def check_org_registration(org_name):
    org_exist = User().check_org_existence(org_name)
    if org_name == '':
        return False
    elif org_exist:
        return True
    else:
        return False


def check_contact_registration(number):
    contact_exist = User().check_contact_existence(number)
    if contact_exist:
        return True
    return False


def save_new_password(email, password):
    hashed_password = hash_password(password)
    User().save_new_password(email,hashed_password)
    return

def get_role(email: str) -> str:
    role = User().get_role(email)
    return role