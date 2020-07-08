__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'

# libraries
import os
from flask import Flask, url_for
from configurations import Configurations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_admin import helpers as admin_helpers

db = SQLAlchemy()
migrate = Migrate()
admin = flask_admin.Admin()
security = Security()

application_directory = os.path.abspath(os.path.dirname(__file__))


def create_app(configuration_class: object = Configurations):
    """
    The :func:`create_app` is the most important method in this library. It starts
    by creating the application, preparing the context, initiating the security measures, etc.

    Parameters
    ----------
    configuration_class: `object`, optional (default=Configurations)
        The configuration is set in this method using an object, and the parameters are defined
        in the configuration object stored in `configurations.py`, which is the default value as well.

    Returns
    ----------
    This method returns the application context and the user datastore object
    """
    app = Flask(__name__)
    app.config.from_object(configuration_class)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    # Create admin
    admin.__init__(
        app,
        'ViSierra',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security._state = security.init_app(app=app, datastore=user_datastore)
    user_datastore = SQLAlchemyUserDatastore(db, user_model=User, role_model=Role)
    with app.app_context():
        @security.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                h=admin_helpers,
                get_url=url_for
            )

    from application.blueprints.authentication import bp as authentication_bp
    app.register_blueprint(authentication_bp)
    from application.blueprints.visualizations import bp as visualization_bp
    app.register_blueprint(visualization_bp)
    from application.blueprints.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from application.blueprints.ml_toolkit import bp as mlkit_bp
    app.register_blueprint(mlkit_bp)
    from application.blueprints.questionnaires import bp as questionnaires_bp
    app.register_blueprint(questionnaires_bp)

    return app, user_datastore


from application.entities import User, Role
