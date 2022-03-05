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