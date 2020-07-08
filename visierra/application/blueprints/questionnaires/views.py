__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credit__ = 'ERLab - CS@UCLA'

import json, pickle
import pandas
import os
from flask import render_template
from flask_admin import BaseView, expose
from application import application_directory
from application.blueprints.questionnaires.forms import OxfordHappinessQuestionnaireForm


class OxfordHappinessQuestionnaireView(BaseView):
    """
    The :class:`OxfordHappinessQuestionnaireView` is an example of our questionnaires.
    """

    @expose('/', methods=['POST', 'GET'])
    def index(self):
        """
        The :meth:`index` method takes care of rendering the information in this view.

        Returns
        ----------
        The output of this method is the rendered template including the requested information.
        """
        questionnaire_info = {
            "title": "Oxford Happiness Questionnaire",
            "description": "Can happiness be measured? Try the following Oxford Questionnaire to find out."
        }

        # rendering the form for this palette
        form = OxfordHappinessQuestionnaireForm()

        # if the form is valid, this happens
        if form.validate_on_submit():
            # calculate oxford happiness score
            survey_record = dict()
            survey_record["first_name"] = form.first_name.data
            survey_record["last_name"] = form.last_name.data
            survey_record["email"] = form.email.data
            survey_record["level_of_education"] = form.level_of_education.data
            survey_record["gender"] = form.gender.data
            survey_record["age"] = form.age.data

            score = 0
            reverse_question_indices = [1, 5, 6, 10, 13, 14, 19, 23, 24, 27, 28, 29]

            for i in range(1, 30):
                if i in reverse_question_indices:
                    survey_record["q{}".format(i)] = 6 - getattr(form, "question{}".format(i)).data
                    score += 6 - getattr(form, "question{}".format(i)).data
                else:
                    survey_record["q{}".format(i)] = getattr(form, "question{}".format(i)).data
                    score += getattr(form, "question{}".format(i)).data

            score = float(score) / 29.0
            survey_record["score"] = score

            path_to_happiness_dataset = os.path.abspath(os.path.join(application_directory, 'warehouse/happiness.pkl'))


            if os.path.isfile(path_to_happiness_dataset):
                with open(path_to_happiness_dataset, 'rb') as handle:
                    dataset_records = pickle.load(handle)
            else:
                dataset_records = []

            dataset_records += [survey_record]

            with open(path_to_happiness_dataset, 'wb') as handle:
                pickle.dump(dataset_records, handle)

            if score <= 2:
                 result = """
                 Not happy. If you answered honestly and got a very low score, you’re probably seeing yourself and your
situation as worse than it really is. I recommend taking the Depression Symptoms test (CES‐D
Questionnaire) at the University of Pennsylvania’s “Authentic Happiness” Testing Center. You’ll have to
register, but this is beneficial because there are a lot of good tests there and you can re‐take them later
and compare your scores.
                 """
            elif score <= 3:
                 result = """
                Somewhat unhappy. Try some of the exercises like the Gratitude Journal & Gratitude Lists,
or the Gratitude Visit; or take a look at the “Authentic Happiness” site.
                """
            elif score < 4:
                 result = """
                Not particularly happy or unhappy. A score of 3.5 would be an exact numerical average of happy and
unhappy responses. Some of the exercises mentioned just above have been tested in scientific studies
and have been shown to make people lastingly happier."""
            elif score == 4:
                 result = """
                Somewhat happy or moderately happy. Satisfied. This is what the average person scores."""

            elif score <= 5:
                 result = """
                Rather happy; pretty happy. Check other score ranges for some of my suggestions."""

            elif score < 6:
                 result = """
                Very happy. Being happy has more benefits than just feeling good. It’s correlated with benefits like
health, better marriages, and attaining your goals. 
soon."""
            else:
                 result = """
                Too happy. Yes, you read that right. Recent research seems to show that there’s an optimal level of
happiness for things like doing well at work or school, or for being healthy, and that being “too happy”
may be associated with lower levels of such things."""


            # rendering the visualization palette with the chosen piechart
            return self.render(
                'admin/show_message.html',
                title="Your Results - Oxford Questionnaire of Happiness",
                description="We hope you are happy deep inside, even if you have not realized that it is the way to go yet!",
                message_title="Score: {:.1f} / 6.0".format(score),
                message_body=result
            )

        # general rendering protocol which happens initially or if no visualization scheme is specified.
        return self.render(
            'admin/questionnaire_board.html',
            form=form,
            questionnaire_info=questionnaire_info
        )
