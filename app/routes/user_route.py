from flask import Blueprint, jsonify, request


user_bp = Blueprint("user", __name__)


@user_bp.get("/")
def getalluser():
    return "all user are here"
