from flask import Blueprint
from application import admin
bp = Blueprint('questionnaires', __name__)
from application.blueprints.questionnaires.views import OxfordHappinessQuestionnaireView
admin.add_view(OxfordHappinessQuestionnaireView(name="Oxford Happiness", endpoint='oxford_happiness_questionnaire', menu_icon_type='fa', menu_icon_value='fa-users',))
