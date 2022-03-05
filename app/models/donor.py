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

    @classmethod
    def donation_stat_foods(cls, session_email):
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        user_id = temp[0]

        query_2 = "select items.quantity from donations inner join items on items.donation_id = donations.donation_id \
        inner join users on users.user_id = donations.donor_id where donations.is_collected = 1 and users.user_id = %s \
        and items.unit = 1"
        cursor.execute(query_2, [user_id])
        results = cursor.fetchall()
        return results

    @classmethod
    def donation_stat_beverages(cls, session_email):
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        user_id = temp[0]

        query_2 = "select items.quantity from donations inner join items on items.donation_id = donations.donation_id \
        inner join users on users.user_id = donations.donor_id where donations.is_collected = 1 and users.user_id = %s \
        and items.unit = 2"
        cursor.execute(query_2, [user_id])
        results = cursor.fetchall()
        return results

    @classmethod
    def donation_stat_food_distributed(cls, session_email):
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        user_id = temp[0]

        query_2 = "select items.quantity from donations inner join items on items.donation_id = donations.donation_id \
        inner join users on users.user_id = donations.donor_id where donations.is_distributed = 1 and users.user_id = %s \
        and items.unit = 1"
        cursor.execute(query_2, [user_id])
        results = cursor.fetchall()
        return results

    @classmethod
    def donation_stat_bev_distributed(cls, session_email):
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        user_id = temp[0]

        query_2 = "select items.quantity from donations inner join items on items.donation_id = donations.donation_id \
        inner join users on users.user_id = donations.donor_id where donations.is_distributed = 1 and users.user_id = %s \
        and items.unit = 2"
        cursor.execute(query_2, [user_id])
        results = cursor.fetchall()
        return results