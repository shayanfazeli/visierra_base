__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credits__ = 'ER Lab - CS@UCLA'


from flask_admin import BaseView, expose
import pandas
import os
from application import application_directory
from application.blueprints.visualizations.forms import VisualizationForm
from flask import render_template
import json
from application.entities import Dataframe
from application.libraries.transformation import transform_dataframe
from application.blueprints.visualizations.visualizations import WalkingPieChartDuringDateRange, ProgressThroughTimeCircularVisualization, ProgressThroughTimeVisualization, WordCloudsVisualization


class TableBoard(BaseView):
    @expose('/')
    def index(self):
        tables = pandas.read_csv(os.path.join(application_directory, 'warehouse/sample_df.csv'))
        return self.render(
            'admin/show_table.html',
            tables=[tables.to_html(classes='data')],
            titles=tables.columns.values
        )


class VisualizationsPortfolio(BaseView):
    @expose('/')
    def index(self):
        with open(os.path.join(application_directory, 'static/meta/visualizations.json')) as handle:
            visualizations = json.load(handle)
        return self.render(
            'admin/visualizations_portfolio.html',
            visualizations=visualizations
        )


class VisualizationPalette(BaseView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        data = None
        visualization_information = {}
        scheme="not specified"
        form = VisualizationForm()
        if form.validate_on_submit():
            rendering_arguments_dict = dict()
            rendering_arguments_dict['template'] = 'admin/visualization_palette.html'

            scheme = form.visualization.data
            rendering_arguments_dict['scheme'] = scheme
            try:
                guide_json = json.loads(str(form.guide.data))
            except:
                return render_template("errors/bad_json.html")

            # preparing the visualization agent
            # according to the selected scheme
            if scheme == "progress_through_time":
                agent = ProgressThroughTimeVisualization(
                    subject=guide_json['subject'],
                    start_date=guide_json['start_date'],
                    end_date=guide_json['end_date'],
                    scheme=scheme,
                    resolution=guide_json['resolution']
                )
            elif scheme == "progress_through_time_circular":
                agent = ProgressThroughTimeCircularVisualization(
                    subject=guide_json['subject'],
                    start_date=guide_json['start_date'],
                    end_date=guide_json['end_date'],
                    scheme=scheme,
                    resolution=guide_json['resolution']
                )
            elif scheme == "walking_chart_during_date_range":
                agent = WalkingPieChartDuringDateRange(
                    subject=guide_json['subject'],
                    start_date=guide_json['start_date'],
                    end_date=guide_json['end_date'],
                    scheme=scheme,
                    resolution=guide_json['resolution']
                )
            elif scheme == "word_clouds":
                agent = WordCloudsVisualization(guide=guide_json)
            else:
                raise NotImplementedError

            # retrieving the visualization specific information
            # that should be relayed to the html template
            # using Jinja2, for example knowing what single js file
            # to include, what is the html subtemplate for this visualization, etc.
            rendering_arguments_dict['visualization_information'] = agent.visualization_information()

            # reading the registered dataframe and performing the requested transformation before
            # proceeding to visualize it...
            dataframe = Dataframe.query.filter_by(name=form.dataframe.data).first()
            data = pandas.read_csv(os.path.join(application_directory, dataframe.relative_path))
            try:
                data = transform_dataframe(dataframe=data, guide=guide_json)
            except Exception as e:
                return render_template("errors/failed_transformation.html")

            # visualization specific sanity checking
            agent.check_dataframe_sanity(dataframe=data)

            # visualization specific morphing to render data consistent with our template
            data = agent.visualization_specific_morphing(dataframe=data)

            # saving to the cache csv
            data.to_csv(os.path.join(application_directory, 'static/warehouse/palette_cache.csv'), index=False)

            # preparing the visualization agent
            # according to the selected scheme
            rendering_arguments_dict['form'] = form
            rendering_arguments_dict['chart_data'] = data

            # any special argument for visualization, comes here
            if scheme == "progress_through_time":
                y_range_l = int(data.loc[:, ['toe', 'flat', 'normal']].to_numpy().ravel().min())
                y_range_u = int(data.loc[:, ['toe', 'flat', 'normal']].to_numpy().ravel().max())
                rendering_arguments_dict['y_range'] = [y_range_l, y_range_u]
                rendering_arguments_dict['x_range'] = [int(data.loc[:, 'timestamp'].min()), int(data.loc[:, 'timestamp'].max())]
            elif scheme == "walking_chart_during_date_range":
                # getting the step layout
                step_layout = agent.step_layout

                # filling the not a number values
                data.fillna(0, inplace=True)

                # piechart dictionary which is to be used in the d3.js script in the html file
                piechart_dict = dict()

                # for each step type this dictionary has to be filled
                for step_type in step_layout:
                    piechart_dict[step_type] = data[step_type][0]

                rendering_arguments_dict['piechart_dict'] = piechart_dict
            elif scheme == "word_clouds":
                agent.generate_word_cloud_picture(data)
            elif scheme == "progress_through_time_circular":
                pass
            else:
                raise NotImplementedError

            return self.render(**rendering_arguments_dict)

        return self.render(
            'admin/visualization_palette.html',
            form=form,
            scheme=scheme,
            visualization_information=visualization_information
        )

    # that the model has to go through, and second, being the information that the plot needs which is specified beforehand, and
    # with the information such as column mappings (note that the plot needs it too).
