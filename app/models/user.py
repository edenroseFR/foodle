from werkzeug.security import check_password_hash
from . import db, cursor


class User():
    def __init__(
        self,
        user_id: str = None,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        email: str = None,
        password: str = None,
        phone_number=None,
        org_name: str = None,
        about: str = None,
        street: str = None,
        barangay: str = None,
        city: str = None,
        image_link: str = None,
        user_role: int = None
    ) -> None:

        self.user_id = user_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.org_name = org_name
        self.about = about
        self.street = street
        self.barangay = barangay
        self.city = city
        self.image_link = image_link
        self.user_role = user_role

    def add_new(self):
        query = f"""
            INSERT INTO users (
                first_name,
                middle_name,
                last_name,
                email,
                about,
                org_name,
                password,
                phone_number,
                street,
                barangay,
                city,
                user_role
            )
            VALUE (
                "{self.first_name}",
                "{self.middle_name}",
                "{self.last_name}",
                "{self.email}",
                "{self.about}",
                "{self.org_name}",
                "{self.password}",
                {self.phone_number},
                "{self.street}",
                "{self.barangay}",
                "{self.city}",
                {self.user_role}
            )
        """
        cursor.execute(query)
        db.commit()
        return None

    def get_role(self, email):
        query = f"""
            SELECT r.role_name
            FROM users u
            JOIN roles r
            ON u.user_role = r.role_id
            WHERE u.email = "{email}"
        """
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result

    def check_credentials(self, email, password):
        username_exist = self.check_email_existence(email)
        if username_exist:
            password_match = self.check_password_match(email, password)
            if password_match:
                return True
            return "Wrong password."
        return "Username does not exist"

    def check_password_match(self, email, password):
        query = f"""
            SELECT password
            FROM users
            WHERE email = "{email}"
        """
        cursor.execute(query)
        result = cursor.fetchone()
        password_from_db = result[0]
        password_match = check_password_hash(password_from_db, password)
        if password_match:
            return True
        return False

    def check_org(self, email):
        role = self.get_role(email)
        if role == "collector":
            return True
        elif role == "indiv-donor":
            return False
        elif role == "org-donor":
            return True

    @staticmethod
    def update_personal_info(user, new_data):
        query = f"""
            UPDATE users
            SET 
                image_link = "{new_data[0]}",
                first_name = "{new_data[1]}",
                middle_name = "{new_data[2]}",
                last_name = "{new_data[3]}",
                phone_number = "{new_data[4]}"
            WHERE
                email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def update_address_info(user, new_data):
        query = f"""
            UPDATE users
            SET 
                street = "{new_data[0]}",
                barangay = "{new_data[1]}",
                city = "{new_data[2]}"
            WHERE
                email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def update_org_inf(user, new_data):
        query = f"""
            UPDATE users
            SET 
                org_name = "{new_data[0]}",
                about = "{new_data[1]}"
            WHERE
                email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def update_password(user, new_data):
        query = f"""
            UPDATE users
            SET password = "{new_data[0]}"
            WHERE email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def update_privacy(user, new_data):
        query = f"""
            UPDATE users
            SET 
                public_profile = "{new_data[0]}",
                show_donor_name = "{new_data[1]}"
            WHERE
                email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def update_notifications(user, new_data):
        query = f"""
            UPDATE users
            SET notifications = "{new_data[0]}"
            WHERE email = "{user}"
        """
        cursor.execute(query)
        db.commit()
        return None

    @staticmethod
    def get_user(email):
        query = f"""
            SELECT image_link,
                   first_name,
                   middle_name,
                   last_name,
                   phone_number,
                   street,
                   barangay,
                   city,
                   password,
                   public_profile,
                   show_donor_name,
                   org_name,
                   about,
                   notifications
            FROM users
            WHERE email = "{email}"
        """
        cursor.execute(query)
        user = list(cursor.fetchone())
        return user

    @staticmethod
    def check_email_existence(email):
        query = f"""
            SELECT first_name
            FROM users
            WHERE email = "{email}"
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
        return False

    @staticmethod
    def check_org_existence(org_name):
        query = f"""
            SELECT first_name
            FROM users
            WHERE org_name = "{org_name}"
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
        return False

    @staticmethod
    def check_contact_existence(number):
        query = f"""
            SELECT first_name
            FROM users
            WHERE phone_number = "{number}"
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return True
        return False

    @staticmethod
    def save_new_password(email, password):
        query = f"""
            UPDATE users
            SET password = "{password}"
            WHERE email = "{email}"
        """
        cursor.execute(query)
        db.commit()
        return None
