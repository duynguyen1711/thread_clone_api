from app import db
from datetime import datetime
from sqlalchemy import Enum
from ..constraints.user_enum import AccountStatus, UserRole


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    avatar_url = db.Column(db.String(256))
    account_status = db.Column(
        Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False
    )
    role = db.Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    deleted_at = db.Column(db.DateTime)
    threads = db.relationship(
        "Thread", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="user", lazy=True, cascade="all, delete-orphan"
    )
