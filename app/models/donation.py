from datetime import date
from urllib.parse import quote_from_bytes
from collections import OrderedDict
from . import cursor, db


class Donation:
    def __init__(self):
        pass

    def add_donation(
        self,
        session_email,
        added_items: list,
        today_datetime,
        t_mode,
        street,
        barangay,
        city,
    ):
        number_of_items = len(added_items)

        query_1 = "select users.user_id from users where users.email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        donor_id = int(temp[0])

        query_2 = "insert into donations(donor_id,datetime_created,transport_mode,number_of_items, street, barangay, city) \
                    values(%s,%s, %s, %s, %s, %s, %s)"
        cursor.execute(
            query_2,
            [donor_id, today_datetime, t_mode, number_of_items, street, barangay, city],
        )
        db.commit()

        query_3 = "select max(donation_id) from donations"
        cursor.execute(query_3)
        temp = cursor.fetchone()
        donation_id = int(temp[0])

        query_4 = "insert into items(donation_id, category, quantity, unit, item_img_url) \
                values (%s, %s, %s, %s, %s)"

        for item in added_items:
            data = [
                donation_id,
                item["category"],
                item["quantity"],
                item["unit"],
                item["item_photo"],
            ]
            cursor.execute(query_4, data)
            db.commit()

    def get_category_options(self):
        query = "select * from categories"
        cursor.execute(query)
        results = cursor.fetchall()

        options = []
        for item in results:
            options.append(tuple(item))

        return options

    def get_tmode_options(self):
        query = "select * from transport_modes"
        cursor.execute(query)
        results = cursor.fetchall()

        options = []
        for item in results:
            options.append(tuple(item))

        return options

    def get_donation_items(cls, donation_id):
        query = f"""
            SELECT c.category_name, 
                   i.quantity, 
                   i.unit, 
                   i.item_img_url
            FROM items i
            JOIN categories c on i.category = c.category_id
            WHERE i.donation_id = {donation_id}
        """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(item) for item in result]
        for item in result:
            if item[2] == "1":
                item[2] = "kilos"
            else:
                item[2] = "liters"
        return result

    def get_donations(self, session_email):
        images = []
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        user_id = cursor.fetchone()[0]

        query_2 = "select donations.donation_id from donations inner join users on users.user_id = donations.donor_id where user_id = %s"

        cursor.execute(query_2, [user_id])
        user_donations = cursor.fetchall()

        query_3 = "select items.item_img_url from items where donation_id = %s"

        for donation in user_donations:
            donation_id = donation[0]
            cursor.execute(query_3, [donation_id])
            items = cursor.fetchall()
            images.append(items)

        return images

    @classmethod
    def get_user_id(cls, session_email):
        query_1 = "select users.user_id from users where email = %s"
        cursor.execute(query_1, [session_email])
        user_id = cursor.fetchone()[0]
        return user_id

    @classmethod
    def show_donation_items(cls, donation_id):
        query = f"""SELECT items.category, items.quantity, items.unit, items.item_img_url from items 
                    where items.donation_id = {donation_id}
                """
        cursor.execute(query)
        items = cursor.fetchall()

        return items

    def collect_verify(cls, donation_id, session_email, today_datetime):
        query_1 = """
        UPDATE donations
        SET is_posted = 0,
            is_collected = 0
        WHERE donation_id = %s
        """
        cursor.execute(query_1, [donation_id])
        db.commit()

        query_1 = "select users.user_id from users where users.email = %s"
        cursor.execute(query_1, [session_email])
        temp = cursor.fetchone()
        donor_id = int(temp[0])

        query_2 = "insert into reserved_donations(donation_id, collector_id, datetime_reserved) values (%s, %s, %s)"
        cursor.execute(query_2, [donation_id, donor_id, today_datetime])
        db.commit()

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

    def get_collectables(self, user_city):
        collectables = OrderedDict()
        query = f"""
            SELECT u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name, 
                   d.donation_id, 
                   d.datetime_created, 
                   tm.mode_name, 
                   d.street, 
                   d.barangay, 
                   d.city,
                   u.image_link
            FROM donations d
            JOIN users u ON d.donor_id = u.user_id
            JOIN transport_modes tm on d.transport_mode = tm.mode_id
            WHERE d.is_posted = 1 AND d.city = '{user_city}'
        """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(item) for item in result]

        for item in result:
            donation_id = item[4]
            donor_name = self.get_donor_name([item[0], item[1], item[2], item[3]])
            donor_image = item[10]
            transport_mode = item[6]
            time_posted = item[5].strftime("%b %d %Y %H:%M:%S")
            location = item[7] + ", " + item[8] + ", " + item[9]
            items = self.get_donation_items(donation_id)
            collectables[donation_id] = {
                "donor_name": donor_name,
                "donor_image": donor_image,
                "time_posted": time_posted,
                "transport_mode": transport_mode,
                "location": location,
                "items": items,
            }

            # data structure of the collectables
            # {
            #     donation_id : {
            #         'donor_name' : 'Juan Luna',
            #         'donor_image' : 'https',
            #         'time_posted' : '0:00:00',
            #         'items' : [['dairy', 2, 'kilos', 'https'], ['dairy', 2, 'kilos', 'https']]
            #     }
            # }
        # Make the latest post appear on top
        collectables = dict(reversed(sorted(collectables.items())))
        return collectables

    def get_donor_name(self, data):
        if data[-1]:
            return data[-1]
        else:
            donor_name = data[0] + " " + data[1] + " " + data[2]
            return donor_name

    @classmethod
    def get_donation_details(cls, donation_id):
        query_1 = f"""Select d.street, d.barangay, d.city, d.transport_mode from donations d 
                Where d.donation_id = {donation_id}"""
        cursor.execute(query_1)
        temp = cursor.fetchone()
        details = {
            "street": temp[0],
            "barangay": temp[1],
            "city": temp[2],
            "t_mode": temp[3],
        }
        return details

    def get_donation_items(self, donation_id):
        query = f"""
            SELECT c.category_name, 
                   i.quantity, 
                   i.unit, 
                   i.item_img_url
            FROM items i
            JOIN categories c on i.category = c.category_id
            WHERE i.donation_id = {donation_id}
        """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(item) for item in result]
        for item in result:
            if item[2] == "1":
                item[2] = "kilos"
            else:
                item[2] = "liters"
        return result

    @classmethod
    def get_collectables_id(cls):
        query_1 = "select donations.donation_id from donations where is_posted = 1"
        cursor.execute(query_1)
        donation_ids = cursor.fetchall()

        return donation_ids

    @classmethod
    def collect_collectables(cls, donation_id):
        query_1 = f"select * from donations where donation_id = {donation_id}"
        cursor.execute(query_1)
        result = cursor.fetchall()

        return result

    @classmethod
    def get_verify_details(cls, donation_id):
        sql = f"select u.first_name, u.middle_name, u.last_name, u.image_link, d.datetime_created, d.street, d.barangay, d.city, tm.mode_name from donations d join users u on d.donor_id = u.user_id join transport_modes tm on d.transport_mode = tm.mode_id where d.donation_id = {donation_id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        date_created = result[4].strftime("%b %d %Y %H:%M:%S")
        result = [str(data) for data in result]
        if result[3] == "None":
            result[3] = ""
        result[4] = date_created

        return result

    @classmethod
    def delete_items(self, donation_id):
        query = f"""DELETE from items where donation_id = {donation_id}"""
        cursor.execute(query)
        db.commit()

    @classmethod
    def update_items(cls, donation_id, added_items: list):
        query = "INSERT INTO items(donation_id, category, quantity, unit, item_img_url) \
                VALUES(%s, %s, %s, %s, %s) "
        for item in added_items:
            data = [
                donation_id,
                item["category"],
                item["quantity"],
                item["unit"],
                item["item_photo"],
            ]
            cursor.execute(query, data)
            db.commit()

    def update_donation(
        cls,
        donation_id,
        added_items,
        today_datetime,
        t_mode,
        number_of_items,
        street,
        barangay,
        city,
    ):
        cls.delete_items(donation_id)
        cls.update_items(donation_id, added_items)

        query = f"""UPDATE donations SET datetime_created = %s , transport_mode = %s, number_of_items = %s , 
                    street = %s, barangay = %s, city = %s WHERE donation_id = %s """
        cursor.execute(
            query,
            [
                today_datetime,
                t_mode,
                number_of_items,
                street,
                barangay,
                city,
                donation_id,
            ],
        )
        db.commit()

    def get_transport_mode_name(self, mode_id):
        query = f"""
            SELECT mode_name
            FROM transport_modes
            WHERE mode_id = '{mode_id}'
        """
        cursor.execute(query)
        mode_name = cursor.fetchone()[0]
        return mode_name

    def get_item_category(self, category_id):
        query = f"""
            SELECT category_name
            FROM categories
            WHERE category_id = '{category_id}'
        """
        cursor.execute(query)
        mode_name = cursor.fetchone()[0]
        return mode_name

    def get_posted_donations(self, user_id, role="donor"):
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
                ORDER BY d.datetime_created DESC
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

        # data structure of the my_posted_donations
        # a = {
        #     1:{
        #         'donor_name' : 'John Doe',
        #         'transport_mode': 'pick-up',
        #         'time_posted': '0:00:00',
        #         'items': [['dairy', '2 kilos', 'https'], ['fats', 'https']],
        #         'distribution_photos' : ['https', 'https'],
        #         'available' : True
        #     }
        # }

    def get_reserved_donations(self, donor_id):
        donations = {}
        query = f"""
            SELECT d.donation_id, 
                   d.transport_mode,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name,
                   r.datetime_reserved,
                   i.category,
                   i.item_img_url,
                   i.quantity,
                   i.unit
                  
            FROM donations d
            JOIN users u ON d.donor_id = u.user_id
            JOIN items i ON i.donation_id = d.donation_id
            JOIN reserved_donations r ON d.donation_id = r.donation_id
            WHERE d.donor_id = {donor_id} AND r.is_collected = 0
            ORDER BY r.reserved_donation_id DESC
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
            if int(item[10]) == 1:
                quantity = "kilo/s"
            else:
                quantity = "liter/s"
            if item[5]:
                donor_name = item[5]
            else:
                donor_name = item[2] + " " + item[3] + " " + item[4]

            if donation_id not in donations:
                donations[donation_id] = {
                    "donor_name": donor_name,
                    "transport_mode": transport_name,
                    "time_posted": time_posted,
                    "items": [[category, item[9], quantity, image]],
                }
            else:
                donations[donation_id]["items"].append(
                    [category, item[9], quantity, image]
                )
        return donations

        # data structure of the my_posted_donations
        # a = {
        #     1:{
        #         'transport_mode': 'pick-up',
        #         'time_posted': '0:00:00',
        #         'items': [['dairy', '2 kilos', 'https'], ['fats', 'https']]
        #     }
        # }

    def get_collected_donations(self, donor_id):
        donations = {}
        query = f"""
            SELECT d.donation_id, 
                   d.transport_mode,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name,
                   c.datetime_collected,
                   i.category,
                   i.item_img_url,
                   i.quantity,
                   i.unit
                  
            FROM donations d
            JOIN users u ON d.donor_id = u.user_id
            JOIN items i ON i.donation_id = d.donation_id
            JOIN collected_donations c ON d.donation_id = c.donation_id
            JOIN reserved_donations r on d.donation_id = r.donation_id
            WHERE d.donor_id = {donor_id} AND r.is_collected = 1 AND d.is_distributed = 0
            ORDER BY c.collected_donation_id DESC
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
            if int(item[10]) == 1:
                quantity = "kilo/s"
            else:
                quantity = "liter/s"
            if item[5]:
                donor_name = item[5]
            else:
                donor_name = item[2] + " " + item[3] + " " + item[4]

            if donation_id not in donations:
                donations[donation_id] = {
                    "donor_name": donor_name,
                    "transport_mode": transport_name,
                    "time_posted": time_posted,
                    "items": [[category, item[9], quantity, image]],
                }
            else:
                donations[donation_id]["items"].append(
                    [category, item[9], quantity, image]
                )
        return donations

        # data structure of the my_posted_donations
        # a = {
        #     1:{
        #         'transport_mode': 'pick-up',
        #         'time_posted': '0:00:00',
        #         'items': [['dairy', '2 kilos', 'https'], ['fats', 'https']]
        #     }
        # }

    def get_distributed_donations(self, donor_id):
        donations = {}
        query = f"""
            SELECT d.donation_id, 
                   d.transport_mode,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name,
                   c.datetime_collected,
                   i.category,
                   i.item_img_url,
                   i.quantity,
                   i.unit
                  
            FROM donations d
            JOIN users u ON d.donor_id = u.user_id
            JOIN items i ON i.donation_id = d.donation_id
            JOIN collected_donations c ON d.donation_id = c.donation_id
            JOIN distributed_donations dt ON d.donation_id = dt.donation_id
            WHERE d.donor_id = {donor_id} AND c.is_distributed = 1
            ORDER BY dt.distributed_donation_id DESC
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
            if int(item[10]) == 1:
                quantity = "kilo/s"
            else:
                quantity = "liter/s"
            if item[5]:
                donor_name = item[5]
            else:
                donor_name = item[2] + " " + item[3] + " " + item[4]

            if donation_id not in donations:
                donations[donation_id] = {
                    "donor_name": donor_name,
                    "transport_mode": transport_name,
                    "time_posted": time_posted,
                    "items": [[category, item[9], quantity, image]],
                }
            else:
                donations[donation_id]["items"].append(
                    [category, item[9], quantity, image]
                )
        return donations

        # data structure of the my_posted_donations
        # a = {
        #     1:{
        #         'transport_mode': 'pick-up',
        #         'time_posted': '0:00:00',
        #         'items': [['dairy', '2 kilos', 'https'], ['fats', 'https']]
        #     }
        # }

    def cancel_reserved_donation(self, donation_id, is_delete):

        query_1 = (
            f"""DELETE from reserved_donations where donation_id = {donation_id}"""
        )
        cursor.execute(query_1)

        if is_delete:
            query_2 = (
                f"""DELETE from collected_donations where donation_id = {donation_id}"""
            )
            cursor.execute(query_2)
            db.commit()
            query_3 = f"""DELETE from items where donation_id = {donation_id}"""
            cursor.execute(query_3)
            db.commit()
            query_4 = f"""DELETE FROM donations where donation_id = {donation_id}"""
            cursor.execute(query_4)
            db.commit()
        else:
            query_5 = f"""UPDATE donations SET donations.is_posted = 1 where donation_id = {donation_id}"""
            cursor.execute(query_5)
            db.commit()

    def get_collected_donation_details(self, donor_id):
        details = {}
        query_1 = f"""SELECT d.donation_id,
                             d.datetime_created,
                             r.datetime_reserved,
                             c.datetime_collected,
                             c.collector_id,
                             d.street,
                             d.barangay,
                             d.city,
                             d.number_of_items,
                             t.mode_name
                    FROM donations d
                    JOIN reserved_donations r on r.donation_id = d.donation_id
                    JOIN collected_donations c on c.donation_id = d.donation_id
                    JOIN transport_modes t on t.mode_id = d.transport_mode 
                    WHERE d.is_collected = 1 AND d.is_distributed = 0 AND d.donor_id= {donor_id}
                    ORDER BY c.collected_donation_id DESC"""
        cursor.execute(query_1)
        result = list(cursor.fetchall())
        result = [list(i) for i in result]

        for detail in result:
            donation_id = detail[0]
            datetime_created = detail[1].strftime("%m/%d/%Y, %H:%M:%S")
            datetime_reserved = detail[2].strftime("%m/%d/%Y, %H:%M:%S")
            datetime_collected = detail[3].strftime("%m/%d/%Y, %H:%M:%S")
            collector_org_name = self.get_collector_org(detail[4])
            location = detail[5] + ", " + detail[6] + ", " + detail[7]
            number_of_items = detail[8]
            t_mode = detail[9]

            if donation_id not in details:
                details[donation_id] = {
                    "datetime_created": datetime_created,
                    "datetime_reserved": datetime_reserved,
                    "datetime_collected": datetime_collected,
                    "collector_org_name": collector_org_name,
                    "location": location,
                    "number_of_items": number_of_items,
                    "transport_mode": t_mode,
                }

        return details

    def get_collector_org(self, collector_id):
        query = f"""
            SELECT u.org_name
            FROM users u
            WHERE u.user_id = {collector_id}
        """
        cursor.execute(query)
        collector = cursor.fetchone()[0]

        return collector

    def get_distributed_donation_details(self, donor_id):
        details = {}
        query_1 = f"""SELECT d.donation_id,
                             d.datetime_created,
                             r.datetime_reserved,
                             c.datetime_collected,
                             db.datetime_distributed,
                             c.collector_id,
                             d.street,
                             d.barangay,
                             d.city,
                             d.number_of_items,
                             t.mode_name
                    FROM donations d
                    JOIN reserved_donations r on r.donation_id = d.donation_id
                    JOIN collected_donations c on c.donation_id = d.donation_id
                    JOIN distributed_donations db on db.donation_id = d.donation_id
                    JOIN transport_modes t on t.mode_id = d.transport_mode 
                    WHERE d.is_distributed = 1 AND d.donor_id= {donor_id}
                    ORDER BY db.distributed_donation_id DESC"""
        cursor.execute(query_1)
        result = list(cursor.fetchall())
        result = [list(i) for i in result]

        for detail in result:
            donation_id = detail[0]
            datetime_created = detail[1].strftime("%m/%d/%Y, %H:%M:%S")
            datetime_reserved = detail[2].strftime("%m/%d/%Y, %H:%M:%S")
            datetime_collected = detail[3].strftime("%m/%d/%Y, %H:%M:%S")
            datetime_distributed = detail[4].strftime("%m/%d/%Y, %H:%M:%S")
            collector_org_name = self.get_collector_org(detail[5])
            location = detail[6] + ", " + detail[7] + ", " + detail[8]
            number_of_items = detail[9]
            t_mode = detail[10]

            if donation_id not in details:
                details[donation_id] = {
                    "datetime_created": datetime_created,
                    "datetime_reserved": datetime_reserved,
                    "datetime_collected": datetime_collected,
                    "datetime_distributed": datetime_distributed,
                    "collector_org_name": collector_org_name,
                    "location": location,
                    "number_of_items": number_of_items,
                    "transport_mode": t_mode,
                }

        return details

    def get_distributed_donation_photo(self, donor_id):
        distributed_donation_photo = {}
        query = f"""SELECT di.donation_id, 
                           di.image_link
            FROM distribution_images di
            JOIN donations d on d.donation_id = di.donation_id
            WHERE d.donor_id = {donor_id} 
            ORDER BY di.image_id DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(i) for i in result]

        for item in result:
            donation_id = item[0]
            photo_url = item[1]

            if donation_id not in distributed_donation_photo:
                distributed_donation_photo[donation_id] = {
                    # 'donation_id': donation_id,
                    "photo_url": [photo_url]
                }
            else:
                distributed_donation_photo[donation_id]["photo_url"].append(photo_url)
        return distributed_donation_photo

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

    @staticmethod
    def get_user_city(session_email):
        query_1 = "select users.city from users where email = %s"
        cursor.execute(query_1, [session_email])
        city = cursor.fetchone()[0]
        return city

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
