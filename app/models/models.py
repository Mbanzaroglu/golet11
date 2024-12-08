from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        # Diğer gerekli alanları ekleyin

    def get_id(self):
        return str(self.id)
