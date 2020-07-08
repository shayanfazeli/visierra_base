from flask import Blueprint
from application import admin
bp = Blueprint('mlkit', __name__)
from application.blueprints.ml_toolkit.views import MachineLearningToolkit
admin.add_view(MachineLearningToolkit(name="ML-Kit", endpoint='ml_kit', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))
