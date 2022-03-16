from . import db
from . import cursor

class Role():
    def get_id(role_name: str = None) -> int:
        query = f'''
            SELECT role_id
            FROM roles
            WHERE role_name = '{role_name}'
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        role_id = int(result[0])
        return role_id
