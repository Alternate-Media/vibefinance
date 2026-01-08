from polyfactory.factories.pydantic_factory import ModelFactory
from backend.models.user import User
from backend.models.session import UserSession


class UserFactory(ModelFactory[User]):
    __model__ = User


class UserSessionFactory(ModelFactory[UserSession]):
    __model__ = UserSession

from backend.models.asset import Asset
from backend.models.balance import BalanceHistory

class AssetFactory(ModelFactory[Asset]):
    __model__ = Asset

class BalanceFactory(ModelFactory[BalanceHistory]):
    __model__ = BalanceHistory
