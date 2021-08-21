from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models.user import User
class Show():
    
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.date = data['date']
        self.description= data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None
        
        
        
    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO shows (title, network, date, description, created_at, updated_at, users_id) VALUES ( %(title)s, %(network)s, %(date)s, %(description)s, NOW(), NOW(), %(users_id)s);"
        
        result = connectToMySQL('shows_schema').query_db(query, data)
        
        
        
    @classmethod
    def get_all_shows(cls):
        query = 'SELECT * FROM shows JOIN users ON shows.users_id = users.id;'
    
        results = connectToMySQL ('shows_schema').query_db(query)
        
        shows = []
        
        for item in results:
            show = cls(item)
            user_data = {
                'id' : item['users_id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item ['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item ['users.updated_at']
            }
            show.user = User(user_data)  
            shows.append(show)
        return shows
    
    @classmethod
    def get_show_by_id(cls, data):
        query = 'SELECT * FROM shows JOIN users ON shows.users_id = users.id WHERE shows.id = %(id)s;'
        
        result = connectToMySQL('shows_schema').query_db(query, data)
        
        show = cls(result[0])
        user_data = {
            'id' : result[0]['users_id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        show.user = User(user_data)
        return show
        
    @classmethod
    def update_show(cls, data):
        query = 'UPDATE shows SET title = %(title)s, network = %(network)s, date = %(date)s, description = %(description)s WHERE id = %(id)s;'
        
        connectToMySQL('shows_schema').query_db(query, data)
        
    
    
    @staticmethod
    def validate_show(data):
    
        is_valid = True
        
        if len(data['title']) < 3:
            flash("Title should be 3 to 32 characters")
            is_valid = False
            
            
        if len(data['description']) < 3:
            flash("Description should be 3 to 32 characters")
            is_valid = False
        
        if len(data['network']) < 3:
            flash("Network should be 3 to 32 characters")
            is_valid = False
        
        return is_valid
    