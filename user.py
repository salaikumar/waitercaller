#  Class created to work with Login Function
#  The class should compulsarily contain the below methods, not sure why. Let's see
class User:
    def __init__(self, email):
        self.email = email
    def get_id(self):
        return self.email
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
