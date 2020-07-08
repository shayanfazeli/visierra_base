__author__ = ["Shayan Fazeli"]
__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from application import db
from flask_security import UserMixin, RoleMixin, current_user

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    """
    The :class:`User` which inherits from :class:`db.Model` provides us with the
    User entity.

    This class contains the following attributes, the `id` to keep the index of user entities.
    `first_name`, `last_name`, `email`, `active`, and `password` which are other characteristics
    of the user along with `roles` associated with each user.

    Note that this and the similar functionalities are developed according to https://github.com/jonalxh/Flask-Admin-Dashboard
    """

    # preparing the attribuets
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User: {} {} ({})>'.format(self.first_name, self.last_name, self.email)


class Role(db.Model, RoleMixin):
    """
    The :class:`Role` helps with assigning a role to each user, or a list or roles. These
    will be useful later if there is difference in types of permissions.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {} (description: {})'.format(self.name, self.description)


class Dataframe(db.Model):
    """
    The :class:`Dataframe` entity helps with registration of dataframes in ViSierra platform. In its attributes,
    there is path variables as well which will be used to read the dataframe.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(1000))
    relative_path = db.Column(db.String(1000))
