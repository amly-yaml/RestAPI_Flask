from werkzeug.security import safe_str_cmp
from user import User

'''users = [
    User(1, 'jake', 'adf')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}
'''

def authentication(username, password):
    user = User.find_by_name(username)
    if user and safe_str_cmp(user.password, password):  # any version work for string format
        return user

def itendify(paylioad):
    user_id = paylioad['identity']
    return User.find_by_id(user_id)
