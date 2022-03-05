from os import stat
from typing import ItemsView
from . import db, cursor

class Collector():

    @staticmethod
    def get_id(email: str) -> int:
        query = f'''
            SELECT user_id
            FROM users
            WHERE users.email = '{email}'
        '''
        cursor.execute(query)
        collector_id = int(cursor.fetchone()[0])
        return collector_id

    @staticmethod
    def get_donors(collector_id: int) -> list:
        donors = {}
        query = f'''
            SELECT u.user_id, 
                   u.image_link,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name,
                   u.about
            FROM collected_donations cd
            JOIN donations d ON cd.donation_id = d.donation_id
            JOIN  users u on d.donor_id = u.user_id
            WHERE cd.collector_id = {collector_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(donor) for donor in result]
        for donor in result:
            org_name = donor[5]
            donor_id = donor[0]
            if org_name and org_name not in donors:
                donor_image = donor[1]
                donor_name = org_name
                donors[donor_name] = [donor_image, donor_id, donor[6]]
            elif org_name == '' and org_name not in donors:
                donor_name = donor[2] + ' ' + donor[3] + ' ' + donor[4]
                donor_image = donor[1]
                donors[donor_name] = [donor_image, donor_id, donor[6]]
        return donors

    def get_to_distribute(self, collector_id: int) -> list:
        query = f'''
            SELECT u.user_id,
                   u.first_name, 
                   u.middle_name, 
                   u.last_name, 
                   u.org_name, 
                   d.donation_id,
                   cd.datetime_collected
            FROM collected_donations cd
            JOIN donations d ON cd.donation_id = d.donation_id
            JOIN  users u on d.donor_id = u.user_id
            WHERE cd.collector_id = {collector_id} and d.is_collected = 1 and d.is_distributed = 0
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(collected) for collected in result]
        to_distribute = []
        for collection in result:
            item = []
            donation_id = collection[5]
            donation_categories = self.get_donation_categories(donation_id)
            org_name = collection[4]
            org_id = collection[0]
            if org_name:
                donor_name = [org_name, org_id]
            else:
                donor_name = [collection[1] + ' ' + collection[2] + ' ' + collection[3], org_id]
            collection_time = collection[-1].strftime("%b %d %Y %H:%M:%S")
            donation_images = self.get_donation_images(donation_id)
            item = [donation_id, donor_name, donation_categories, collection_time, donation_images]
            to_distribute.append(item)
        return to_distribute

    def get_donation_images(self, donation_id) -> list[str]:
        query = f'''
            SELECT item_img_url
            FROM items
            WHERE donation_id = {donation_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [str(img[0]) for img in result]
        return result

    def get_donation_categories(self, donation_id):
        categories = ''
        query = f'''
            SELECT c.category_name
            FROM items i
            JOIN categories c ON c.category_id = i.category
            WHERE i.donation_id = {donation_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [cat[0] for cat in result]
        for i in result:
            categories += i + ', '
        categories = categories[:-2]
        return categories