from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email


class OxfordHappinessQuestionnaireForm(FlaskForm):
    """
    OxfordHappinessQuestionnaireForm
    ============

    This form is going to read the data input by the medical practitioners trying
    to monitor shoes' progress for each patient.
    """
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired(), Email()])

    country = StringField("Country", validators=[DataRequired()])

    level_of_education = SelectField(
        "Level of Education",
        choices=[
            ('High School', 'High School'),
            ('College', 'College'),
            ('Master', 'Master'),
            ('Doctorate', 'Doctorate'),
            ('Post-Doctorate', 'Post-Doctorate'),
        ],
        validators=[DataRequired()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ('male', 'Male'),
            ('female', 'female'),
            ('other', 'Other')
        ],
        validators=[DataRequired()]
    )

    age = IntegerField("Age", validators=[DataRequired()])

    question1 = SelectField(
        "I do not feel particularly pleased with the way I am",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ]
    )

    question2 = SelectField(
        "I am intensely interested in other people.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ]
    )

    question3 = SelectField(
        "I feel that life is very rewarding.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question4 = SelectField(
        "I have very warm feelings towards almost everyone.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question5 = SelectField(
        "I rarely wake up feeling rested.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question6 = SelectField(
        "I am not particularly optimistic about the future.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question7 = SelectField(
        "I find most things amusing.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question8 = SelectField(
        "I am always committed and involved.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question9 = SelectField(
        "Life is good.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question10 = SelectField(
        "I do not think that the world is a good place.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question11 = SelectField(
        "I laugh a lot.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question12 = SelectField(
        "I am well satisfied about everything in my life.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question13 = SelectField(
        "I do not think that I look attractive.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question14 = SelectField(
        "There is a gap between what I would like to do and what I have done.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question15 = SelectField(
        "I am very happy.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question16 = SelectField(
        "I find beauty in some things.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question17 = SelectField(
        "I always have a cheerful effect on others.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question18 = SelectField(
        "I can fit in (find time for) everything that I want to.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question19 = SelectField(
        "I feel that I am not especially in control of my life.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question20 = SelectField(
        "I feel able to take anything on.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question21 = SelectField(
        "I feel fully mentally alert.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question22 = SelectField(
        "I often experience joy and elation.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question23 = SelectField(
        "I do not find it easy to make decisions.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question24 = SelectField(
        "I do not have a particular sense of meaning and purpose in my life.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question25 = SelectField(
        "I feel I have a great deal of energy.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question26 = SelectField(
        "I usually have a good influence on events.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    question27 = SelectField(
        "I do not have fun with other people.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question28 = SelectField(
        "I do not feel particularly healthy.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )
    question29 = SelectField(
        "I do not have particularly happy memories of the past.",
        coerce=int,
        choices=[
            (1, 'Strongly Disagree'),
            (2, 'Moderately Disagree'),
            (3, 'Slightly Disagree'),
            (4, 'Slightly Agree'),
            (5, 'Moderately Agree'),
            (6, 'Strongly Agree')
        ],
        validators=[]
    )

    submit = SubmitField('Proceed')