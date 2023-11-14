from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt
from models import (
    User,
    BASE
)
delete_message = 'user deleted successfully'
create_message = 'user created successfully'


class DatabaseHelper:
    """a database class that creates the session and manages it"""
    
    def __init__(self) -> None:
        self._engine = create_engine("mysql://kingsley_profile_db:kingsley_super_user@localhost/profile_db")
        BASE.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """create the session"""
        if self.__session is None:
            database_sesssion = sessionmaker(bind=self._engine, expire_on_commit=False)
            self.__session = database_sesssion()
        return self.__session
    
    def hash_password(self, password):
        """returns bytes from hashed password"""
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_pw

    def verify_password(self, hashed, password):
        """verify password to access user profile using argon2"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def verify_credentials(self, **kwargs):
        """verify user credentials"""
        if not kwargs:
            raise InvalidRequestError('arguments not specified')
        user_profile_table = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in user_profile_table:
                return False
            if not isinstance(kwargs[key], str):
                return False
        return True

    def create_user_profile(self, email, password, username):
        """create a user profile in the database"""
        validator = self.verify_credentials(email=email, password=password, username=username)
        if not validator:
            raise ValueError("invalid credentials")
        password = self.hash_password(password)
        new_user = User(email=email, password=password, username=username)
        try:
            self._session.add(new_user)
            self._session.commit()
            return create_message
        except Exception as exc:
            self._session.rollback()
            raise exc

    def edit_user_profile(self, email, **kwargs):
        """edit the user profile"""
        try:
            user = self.get_user_profile(email=email)
            for k, v in kwargs.items():
                setattr(user, k, v)
            self._session.commit()
        except Exception as exc:
            self._session.rollback()
            raise exc
        
    def get_user_profile(self, **kwargs):
        """get the current user profile"""
        validator = self.verify_credentials(**kwargs)
        if not validator:
            raise ValueError("invalid credential")
        user_profile = self._session.query(User).filter_by(**kwargs).first()
        if user_profile is None:
            raise NoResultFound("user not found")
        return user_profile

    def delete_user_profile(self, user_id):
        """delete the user profile"""
        try:
            user = self.get_user(id=user_id)
            self._session.delete(user)
            self._session.commit()
            return delete_message
        except Exception as exc:
            self._session.rollback()
            raise exc
