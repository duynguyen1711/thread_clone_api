from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"
    DELETED = "DELETED"


class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
