from flask import Blueprint
from application import admin, db
bp = Blueprint('auth', __name__)
from application.blueprints.authentication.views import MyModelView, UserView
from application.entities import Role, User

# registration of views
admin.add_view(MyModelView(Role, db.session, category="Team"))
admin.add_view(UserView(User, db.session, category="Team"))

