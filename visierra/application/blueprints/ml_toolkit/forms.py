__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError
import json


class MLKitForm(FlaskForm):
    """
    The :class:`MLKitForm` builds the main form for the ViSierra's ML-Toolkit, allowing us to
    explore a registered dataframe with machine learning techniques and observe the confusion matrix
    in the end.
    """
    scheme = StringField('Scheme', validators=[DataRequired()])
    dataframe = StringField('Dataframe', validators=[DataRequired()])
    feature_columns = StringField('Feature Columns', validators=[DataRequired()])
    label_column = StringField('Label Column', validators=[DataRequired()])
    hidden_layer_config = StringField('Hidden Layer Configurations', validators=[DataRequired()])
    pca = IntegerField('PCA Dimension', validators=[DataRequired()], default=0)
    guide = TextAreaField(
        'Guide',
        validators=[],
        default="""
                {
                    "transformations": [],
                    "column_mapping": {}
                }
            """
    )
    submit = SubmitField('Proceed')

    def validate_feature_columns(self, feature_columns):
        """
        The validator for the feature columns

        Parameters
        ----------
        feature_columns: `str`, required
            This value comes for the attribute the value of which is provided in the form.
        """
        feature_columns = feature_columns.data
        if ' ' in list(feature_columns):
            raise ValidationError("Please remove all of the spaces.")

        if not (feature_columns[0] == '[' and feature_columns[-1] == ']'):
            raise ValidationError("Correct format is: [name1,name2,name3]")

    def validate_hidden_layer_config(self, hidden_layer_config):
        """
        The validator for the hidden_layer_config

        Parameters
        ----------
        hidden_layer_config: `str`, required
            This value comes for the attribute the value of which is provided in the form.
        """
        hidden_layer_config = hidden_layer_config.data
        if ' ' in list(hidden_layer_config):
            raise ValidationError("Please remove all of the spaces.")

        if not (hidden_layer_config[0] == '[' and hidden_layer_config[-1] == ']'):
            raise ValidationError("Correct format is: [1,1,1]")

        values = hidden_layer_config[1:-1].split(',')
        try:
            values = [int(e) for e in values]
        except:
            raise ValidationError("Bad input for the hidden layer configuration")

    def validate_guide(self, guide):
        """
        This method validates whether or not the guide provided is a valid json

        Parameters
        ----------
        guide: `str`, required
            The `str` format JSON that has been inserted into the text area
        """
        try:
            tmp = json.loads(guide.data)
        except:
            raise ValidationError('Please enter a JSON string here.')

        if not (
                ("column_mapping" in tmp.keys()) and ("transformations" in tmp.keys())
        ):
            raise ValidationError('Please make sure to include transformations and column_mapping in your JSON.')