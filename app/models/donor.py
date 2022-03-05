from os import stat
from . import db, cursor

class Donor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_donor_details(session_email):
        query = "SELECT * FROM users where email = %s"
        cursor.execute(query, [session_email])
        keys = [
            "user_id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "org_name",
            "about",
            "street",
            "barangay",
            "city",
            "image_link",
            "user_role",
            "public_profile",
            "show_donor_name",
            "notifications",
        ]
        values = cursor.fetchone()
        if values != None:
            results = {keys[i]: values[i] for i in range(len(keys))}
            return results
        else:
            return None

    @staticmethod
    def get_donor_id(session_email):
        query = f"""
            SELECT user_id
            FROM users
            WHERE email = '{session_email}'
        """
        cursor.execute(query)
        donor_id = cursor.fetchone()[0]
        return donor_id