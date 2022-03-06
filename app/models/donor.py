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

    def get_my_donations(self, user_id, role="donor"):
        donations = {}
        if role == "donor":
            query = f"""
                SELECT 
                    d.donation_id, 
                    d.transport_mode,
                    u.first_name, 
                    u.middle_name, 
                    u.last_name, 
                    u.org_name,
                    d.datetime_created, 
                    i.category,
                    i.item_img_url,
                    i.quantity,
                    i.unit
                FROM donations d
                JOIN users u ON d.donor_id = u.user_id
                JOIN items i ON i.donation_id = d.donation_id
                WHERE d.donor_id = {user_id} and is_posted = 1
            """
        else:
            query = f"""
                SELECT 
                    d.donation_id, 
                    d.transport_mode,
                    u.first_name, 
                    u.middle_name, 
                    u.last_name, 
                    u.org_name,
                    d.datetime_created, 
                    i.category,
                    i.item_img_url,
                    i.quantity,
                    i.unit
                FROM collected_donations cd
                JOIN donations d ON cd.donation_id = d.donation_id
                JOIN users u ON cd.collector_id = u.user_id
                JOIN items i ON i.donation_id = d.donation_id
                WHERE cd.collector_id = {user_id}
            """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(i) for i in result]

        for item in result:
            donation_id = item[0]
            transport_name = self.get_transport_mode_name(item[1])
            category = self.get_item_category(item[7])
            image = item[8]
            time_posted = item[6].strftime("%m/%d/%Y, %H:%M:%S")
            distribution_photos = []
            available = False

            # Concatenate quantity and unit
            if int(item[10]) == 1:
                quantity = "kilo/s"
            else:
                quantity = "liter/s"

            if donation_id not in donations:
                # Check for organization_name
                if item[5]:
                    donor_name = item[5]
                else:
                    donor_name = item[2] + " " + item[3] + " " + item[4]

                # Check donation status
                status = self.get_status(donation_id)
                if status == "distributed":  # get distribution photos
                    distribution_photos = self.get_distribution_photos(donation_id)
                elif status == "available":  # set available to True
                    available = True

                donations[donation_id] = {
                    "donor_name": donor_name,
                    "transport_mode": transport_name,
                    "time_posted": time_posted,
                    "items": [[category, item[9], quantity, image]],
                    "distribution_photos": distribution_photos,
                    "available": available,
                }
            else:
                donations[donation_id]["items"].append(
                    [category, item[9], quantity, image]
                )
        return donations

    def get_transport_mode_name(self, mode_id):
        query = f"""
            SELECT mode_name
            FROM transport_modes
            WHERE mode_id = '{mode_id}'
        """
        cursor.execute(query)
        mode_name = cursor.fetchone()[0]
        return mode_name

    def get_status(self, donation_id):
        query = f"""
            SELECT is_posted, 
                   is_collected, 
                   is_distributed
            FROM donations 
            WHERE donation_id = {donation_id}
        """
        cursor.execute(query)
        status = list(cursor.fetchall()[0])
        if status[0]:  # Still available for grab
            return "available"
        elif status[2]:  # Already distributed
            return "distributed"
        else:  # Not distributed but already collected
            return "collected"

    def get_distribution_photos(self, donation_id):
        query = f"""
            SELECT image_link
            FROM distribution_images
            WHERE donation_id = {donation_id}
        """
        cursor.execute(query)
        images = cursor.fetchall()
        images = [str(image[0]) for image in images]
        return images

    def get_item_category(self, category_id):
        query = f"""
            SELECT category_name
            FROM categories
            WHERE category_id = '{category_id}'
        """
        cursor.execute(query)
        mode_name = cursor.fetchone()[0]
        return mode_name

    @staticmethod
    def delete_donation(donation_id):
        query1 = f"""
            DELETE FROM donations
            WHERE donation_id = {donation_id}
        """
        query2 = f"""
            DELETE FROM items
            WHERE donation_id = {donation_id}
        """
        cursor.execute(query2)
        db.commit()
        cursor.execute(query1)
        db.commit()
        return None

    @staticmethod
    def get_collectors(session_email) -> list:
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        user_id = temp[0]

        collectors = {}
        query = f"""
            SELECT u.user_id,
                   u.image_link,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name,
                   u.about
            FROM collected_donations cd
            JOIN users u on cd.collector_id = u.user_id
            JOIN donations d ON cd.donation_id = d.donation_id
            WHERE d.donor_id = {user_id} AND d.is_collected = 1
        """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(collector) for collector in result]
        for collector in result:
            collector_image = collector[1]
            org_name = collector[5]
            collector_id = collector[0]
            if org_name and org_name not in collectors:
                collector_name = org_name
                collectors[collector_name] = [
                    collector_image,
                    collector_id,
                    collector[6],
                ]
            elif not org_name:
                collector_name = collector[2] + " " + collector[3] + " " + collector[4]
                if collector_name not in collectors:
                    collectors[collector_name] = [
                        collector_image,
                        collector_id,
                        collector[6],
                    ]
        return collectors

    @staticmethod
    def get_parent_orgs(user_id):
        query = f'''
            select users.org_name from
            members join users
            on users.user_id=members.collector_id and members.user_id={user_id};
        '''
        cursor.execute(query)
        parent_orgs = cursor.fetchall()
        
        return parent_orgs