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

    @staticmethod
    def set_distribute_to_true(donation_id):
        query1 = f'''
            UPDATE donations
            SET is_distributed = '1'
            WHERE donation_id = {donation_id};
        '''
        query2 = f'''
            UPDATE collected_donations
            SET is_distributed = '1'
            WHERE donation_id = {donation_id};
        '''
        cursor.execute(query1)
        db.commit()
        cursor.execute(query2)
        db.commit()
        return None

    def get_items_to_collect(self,collector_id):
        query = f'''
            SELECT 
                u.user_id,
                u.first_name, 
                u.middle_name, 
                u.last_name, 
                u.org_name,
                rd.datetime_reserved,
                d.donation_id, 
                d.street,
                d.barangay,
                d.city,
                d.transport_mode
            FROM reserved_donations rd
            JOIN donations d ON rd.donation_id = d.donation_id
            JOIN  users u on d.donor_id = u.user_id
            WHERE rd.collector_id = {collector_id} and rd.is_collected = 0
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(reserve) for reserve in result]
        to_distribute = []
        for donation in result:
            item = []
            donation_id = donation[6]
            org_name = donation[4]
            org_id = donation[0]
            donation_categories = self.get_donation_categories(donation_id)
            if org_name:
                donor_name = [org_name, org_id]
            else:
                donor_name = [donation[1] + ' ' + donation[2] + ' ' + donation[3], org_id]
            reserve_time = donation[5].strftime("%b %d %Y %H:%M:%S")
            collection_address = donation[7] + ', ' + donation[8] + ', ' + donation[9]
            transport_mode = self.get_transport_mode_name(donation[-1])
            donation_images = self.get_donation_images(donation_id)
            item = [donation_id, donor_name, donation_categories, reserve_time, collection_address, transport_mode, donation_images]
            to_distribute.append(item)
        return to_distribute

    def get_transport_mode_name(self,mode_id):
        query = f'''
            SELECT mt.mode_name
            FROM transport_modes mt
            WHERE mt.mode_id = {mode_id}
        '''
        cursor.execute(query)
        name = cursor.fetchone()[0]
        return name

    @staticmethod
    def set_collected_to_true(donation_id, collector_id, datetime_collected):
        query1 = f'''
            UPDATE donations
            SET is_collected = '1'
            WHERE donation_id = {donation_id};
        '''
        query2 = f'''
            INSERT INTO collected_donations(
                donation_id, 
                collector_id, 
                datetime_collected
            )
            VALUE (
                {donation_id},
                {collector_id},
                '{datetime_collected}'
            )
        '''
        query3 = f'''
            UPDATE reserved_donations
            SET is_collected = '1'
            WHERE donation_id = {donation_id};
        '''
        cursor.execute(query1)
        db.commit()
        cursor.execute(query2)
        db.commit()
        cursor.execute(query3)
        db.commit()
        return None

    def get_completed_collections(self, user_id):
        query = f'''
                SELECT 
                    donation_id,
                    datetime_distributed
                FROM distributed_donations
                WHERE collector_id = {user_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [list(reserve) for reserve in result]
        completed = []
        for donation in result:
            item = []
            completed_ID = [data[0] for data in completed]
            donation_id = donation[0]
            if donation_id not in completed_ID:
                donation_categories = self.get_donation_categories(donation_id)
                distribution_imgs = self.get_distribution_images(donation_id)
                donor_name = self.get_donor_name(donation_id)
                donation_items = self.get_donation_images(donation_id)
                completion_time = donation[1].strftime("%b %d %Y %H:%M:%S")
                item = [donation_id, donor_name, donation_categories, completion_time, distribution_imgs, donation_items]
                completed.append(item)
        return completed

    @staticmethod
    def save_distribution_images(donation_id: int, images: list[str]):
        for image in images:
            if image != '':
                query = f'''
                    INSERT INTO distribution_images(donation_id, image_link)
                    VALUE ({donation_id}, '{image}')
                '''
                cursor.execute(query)
                db.commit()
        return None

        def get_distribution_images(self, donation_id) -> list[str]:
        query = f'''
            SELECT image_link
            FROM distribution_images
            WHERE donation_id = {donation_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [str(img[0]) for img in result]
        return result

    @staticmethod
    def record_distribution(donation_id, collector_id, time_created):
        query = f'''
            INSERT INTO distributed_donations (
                donation_id,
                collector_id,
                datetime_distributed
            )
            VALUE (
                {donation_id},
                {collector_id},
                '{time_created}'
            )
        '''
        cursor.execute(query)
        db.commit()
        return None

    def get_donor_name(self, donation_id):
        query = f'''
            SELECT u.first_name,
                   u.middle_name,
                   u.last_name,
                   u.org_name,
                   u.user_id
            FROM donations d
            JOIN users u ON d.donor_id = u.user_id
            WHERE donation_id = {donation_id}
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        result = [str(col) for col in result[0]]
        user_id = result[4]
        if result[3]:
            return [result[3], user_id]
        else:
            return [result[0] + ' ' + result[1] + ' ' + result[2], user_id]
    
    @staticmethod
    def set_collected_to_false(donation_id):
        query1 = f'''
            UPDATE donations
            SET is_collected = '0'
            WHERE donation_id = {donation_id}
        '''

        query2 = f'''
            DELETE FROM reserved_donations
            WHERE donation_id = {donation_id}
        '''

        query3 = f'''
            UPDATE donations SET is_posted = '1'
            WHERE donation_id = {donation_id}
        '''

        cursor.execute(query1)
        db.commit()
        cursor.execute(query2)
        db.commit()
        cursor.execute(query3)
        db.commit()
        return None

    def get_total_food_bev_distributed(self, email_address):
        collector_id = self.get_id(email_address)
        query = f'''
            SELECT SUM(i.quantity)
            FROM distributed_donations dd
            JOIN items i ON dd.donation_id = i.donation_id
            WHERE dd.collector_id = {collector_id}
        '''
        cursor.execute(query)
        total = cursor.fetchone()[0]
        return total