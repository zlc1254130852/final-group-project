from database_helper import DatabaseHelper

db_helper = DatabaseHelper()

email = 'kingsley@gmail.com'
password = 'kingsleypassword'
username = 'kingsley john'

try:
    creation_message = db_helper.create_user_profile(email, password, username)
    print(creation_message)
except Exception:
    print('user exist')
    
try:
    user = db_helper.get_user_profile(email=email)
    print(f'email: {user.email}\npassword: {user.password}\nusername: {user.username}\nid: {user.id}\nphone: {user.phone_number}\naddress: {user.address}')
    db_helper.edit_user_profile(email=email, phone_number="+23456556655", address="California, U.S.A")
    user = db_helper.get_user_profile(email=email)
    print(f'email: {user.email}\npassword: {user.password}\nusername: {user.username}\nid: {user.id}\nphone: {user.phone_number}\naddress: {user.address}')
except Exception:
    print('user does not exist')
