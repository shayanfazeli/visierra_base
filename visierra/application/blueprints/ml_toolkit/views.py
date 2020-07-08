__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'

from flask import url_for
from flask_admin import BaseView, expose
import pandas
import os
from application import application_directory
from application.blueprints.ml_toolkit.forms import MLKitForm
from flask import render_template
import json
from application.entities import Dataframe
from application.libraries.transformation import transform_dataframe
from application.libraries.ml_toolkit.utilities import prepare_the_dataframe_for_ml, ffnn_experiment


class MachineLearningToolkit(BaseView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        scheme = "not specified"
        form = MLKitForm()
        if form.validate_on_submit():
            scheme = form.scheme.data
            feature_columns = form.feature_columns.data
            feature_columns = feature_columns[1:-1].split(',')
            hidden_layer_config = form.hidden_layer_config.data
            hidden_layer_config = [int(e) for e in hidden_layer_config[1:-1].split(',')]
            hidden_layer_config = tuple(hidden_layer_config)
            label_column = form.label_column.data
            pca_dimension = form.pca.data
            guide_json = json.loads(str(form.guide.data))
            dataframe = Dataframe.query.filter_by(name=form.dataframe.data).first()
            data = pandas.read_csv(os.path.join(application_directory, dataframe.relative_path))

            try:
                data = transform_dataframe(dataframe=data, guide=guide_json)
            except Exception as e:
                return render_template("errors/failed_transformation.html")

            # saving cache if needed
            # data.to_csv(os.path.join(application_directory, 'warehouse/cache/mltoolkit_cache.csv'))
            X_train, y_train, X_test, y_test, original_label_layout = prepare_the_dataframe_for_ml(
                input_dataframe=data,
                label_column=label_column,
                feature_columns=feature_columns
            )

            ffnn_experiment(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                list_of_labels=original_label_layout,
                perform_pca=(pca_dimension>0),
                pca_dim=pca_dimension,
                hidden_layer_config=hidden_layer_config)

            return self.render(
                'admin/ml_kit.html',
                image_url=url_for('static', filename='ml_toolkit/ffnn_experiment.png'),
                scheme=scheme,
                form=form
            )
        return self.render(
            'admin/ml_kit.html',
            scheme=scheme,
            form=form,
            image_url=url_for('static', filename='ml_toolkit/default.png')
        )
