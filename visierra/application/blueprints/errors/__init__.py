from flask import Blueprint
bp = Blueprint('errors', __name__)
from application.blueprints.errors import handlers
