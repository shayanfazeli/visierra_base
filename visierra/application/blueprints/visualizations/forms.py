__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
import json


class VisualizationForm(FlaskForm):
    """
    The :class:`VisualizationForm` builds the main visualization form which is going to be shown
    in the visualization palette. The attributes are the dataframe name, visualization name, and
    the guide JSON data. This, obviously, can be rewritten as more concise forms for different
    particular applications.
    """
    visualization = StringField('Visualization', validators=[DataRequired()])
    dataframe = StringField('Dataframe', validators=[DataRequired()])
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
    submit = SubmitField('Visualize')

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
