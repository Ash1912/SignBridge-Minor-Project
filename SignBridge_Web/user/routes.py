from app import app
from user.models import User
from utils import show_window

# @app.route('/user/signup', methods=['POST'])
# def signup():
#     user = User()
#     return user.signup()

# # @app.route('/user/signout')
# # def signout():
# #     return User().signout()

# @app.route('/user/login', methods=['POST'])
# def login():
#     return User().login()
#     x = User().login()
#     print(x)
#     return x
