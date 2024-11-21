#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first user found with the given filters.
        """
        try:
            query = self._session.query(User)
            for key, value in kwargs.items():
                if not hasattr(User, key):
                    raise InvalidRequestError()
                query = query.filter(getattr(User, key) == value)
            user = query.one()
            return user
        except NoResultFound:
            raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes based on the provided keyword arguments.
        Args:
            user_id (int): ID of the user to update.
            **kwargs: Arbitrary keyword arguments to update user attributes.
        Raises:
            ValueError: If an invalid attribute is provided.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound()
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            setattr(user, key, value)
        self._session.commit()
