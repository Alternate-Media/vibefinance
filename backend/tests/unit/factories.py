from polyfactory.factories.pydantic_factory import ModelFactory
from backend.models.user import User
from backend.models.session import UserSession


class UserFactory(ModelFactory[User]):
    __model__ = User


class UserSessionFactory(ModelFactory[UserSession]):
    __model__ = UserSession
