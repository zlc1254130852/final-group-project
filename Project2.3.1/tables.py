from setting import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    # the salt is a random code used to encrypt cookie info