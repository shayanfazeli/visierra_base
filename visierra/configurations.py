__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'

# libraries
import os
from dotenv import load_dotenv

# preparing some inner variables
base_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_directory, '.env'))


class Configurations(object):
    """
    The :class:`Configurations` holds the main configuration parameters used in ViSierra. The main
    configurations worth mentioning are the secret key which is used mainly in the authentication blueprint, and
    the database parameters especially where the SQLite database is to be saved.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'visierra_is_secret_Key23'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_directory, 'visierra_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['shayan@cs.ucla.edu']
    LANGUAGES = ['en']
    VISUALIZATIONS_PER_PAGE=10
    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "YOUR KEY"
    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

