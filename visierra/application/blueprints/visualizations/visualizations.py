__author__ = 'Shayan Fazeli'
__email__ = 'shayan@cs.ucla.edu'
__credit__ = 'ERLab - CS@UCLA'

import pandas
from overrides import overrides
from typing import Dict, Any
from application import application_directory
import os
from copy import deepcopy
import numpy
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


class VisualizationBase:
    """
    Base Visualization Class
    ==========
    For every visualization, the developer needs to inherit from this class
    and implement its methods, paving the way for the user to call
    and use their visualizations effectively.

    """

    def __init__(self, guide: Dict[str, Any] = dict()):
        # the constructor
        self.guide = guide
        pass

    def check_dataframe_sanity(self, dataframe: pandas.DataFrame):
        """
        This method is responsible to check whether or not the dataframe complies
        with the constraints that a dataframe should comply to if it is to be used for
        the specified visualization. For example, it might need a 'x1', and 'x2' fields
        of type 'float' and with no not a number value in any of them.

        Parameters
        ----------
        dataframe: `pandas.DataFrame`, required
            The input dataframe
        """
        raise NotImplementedError

    def visualization_specific_morphing(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        According to the type of the visualization (along with any other new
        parameter that is set using the constructor in it, user can modify this effectively)
        we need certain set of morphing applied on the system. For example, we might need to use
        a date column, to quantize day-level dates to month-level values, and then use them
        for a "monthly"-based version of a "monthly progress" tracker visualization.

        Parameters
        ----------
        dataframe: `pandas.DataFrame`, required
            The input dataframe

        Returns
        ----------
        The output of this method is the now-altered instance of `pandas.DataFrame`.
        """
        raise NotImplementedError

    def help(self) -> str:
        """
        Each visualization must implement a "help" method which upon calling outputs the specifics of the
        visualization, what is expected of it and what it needs. These will help the callers to modify
        or select their dataframes according to the visualizations' needs.

        Returns
        ----------
        Alongside printing, it should also return the `str` instance of the message to be printed.
        """
        raise NotImplementedError

    def visualization_information(self) -> Dict[str, Any]:
        """
        This method returns a `Dict[str, Any]` instance including
        the information regarding the specific chosen visualization which
        is to be used by jinja in the html templates.
        """
        raise NotImplementedError


class ProgressThroughTimeVisualization(VisualizationBase):
    """
    The :class:`ProgressThroughTimeVisualization` is provided to visualize the time-series
    trajectory of walking style for a selected subject.
    """

    def __init__(self,
                 subject: str,
                 start_date: str,
                 end_date: str,
                 scheme: str,
                 resolution: str):
        """
        The constructor method of :class:`ProgressThroughTimeVisualization`

        Parameters
        ----------
        subject: `str`, required
            The subject id (e.g. `TW06NA`)
        start_date: `str`, required
            The start date in `yyyy-mm-dd` format
        end_date: `str`, required
            The end date in `yyyy-mm-dd` format
        scheme: `str`, required
            The visualization scheme
        resolution: `str`, required
            The choices are `day`, `month`, and `year`
        """
        super(ProgressThroughTimeVisualization, self).__init__()
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date
        self.scheme = scheme
        self.resolution = resolution

    @overrides
    def check_dataframe_sanity(self, dataframe: pandas.DataFrame) -> None:
        """
        Please refer to the method's description in parent class's documentation.
        """
        columns = dataframe.columns.tolist()
        assert "timestamp" in columns
        assert "step_type" in columns
        assert "number_of_steps" in columns

    @overrides
    def visualization_specific_morphing(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Please refer to the method's description in parent class's documentation.
        """
        step_layout = [
            'toe',
            'flat',
            'normal'
        ]

        # copying the dataframe
        output = deepcopy(dataframe)

        def quantize_date(date: str, resolution: str):
            """
            This mini function is for date quantization

            Parameters
            ----------
            date: `str`, required
                The string of date in `yyyy-mm-dd` format
            resolution: `str`, required
                The resolution, which is either `month` or `year`

            Returns
            -----------
            This method returns the quantized month as a `yyyy-mm` instance of `str`, or other types
            of quantized `str` outputs.
            """
            date = date.replace('_', '-')
            date_parts = date.split('-')

            if resolution == 'year':
                return '-'.join(date_parts[:1])
            elif resolution == 'month':
                return '-'.join(date_parts[:2])
            elif resolution == 'day':
                return '-'.join(date_parts[:3])
            else:
                raise NotImplementedError

        # using the internal :meth:`quantize_date`, the dates are quantized
        output["timestamp"] = output["timestamp"].apply(
            lambda x: int(quantize_date(x, self.resolution).replace('-', ''))
        )

        start_date_parts = self.start_date.split('-')
        end_date_parts = self.end_date.split('-')
        if self.resolution == "year":
            timestamp_lowerbound = int(start_date_parts[0])
            timestamp_upperbound = int(end_date_parts[0])
        elif self.resolution == "month":
            timestamp_lowerbound = int(''.join(start_date_parts[:2]))
            timestamp_upperbound = int(''.join(end_date_parts[:2]))
        elif self.resolution == "day":
            timestamp_lowerbound = int(''.join(start_date_parts[:3]))
            timestamp_upperbound = int(''.join(end_date_parts[:3]))
        else:
            raise NotImplementedError

        output = output[output['timestamp'] <= timestamp_upperbound]
        output = output[output['timestamp'] >= timestamp_lowerbound]

        # forming the morphed dataframe and filling the not a numbers
        for step_type in step_layout:
            output[step_type] = output[output['step_type'] == step_type]['number_of_steps']
            output[step_type].fillna(0, inplace=True)

        # sorting by timestamp strings
        output = output.sort_values(by='timestamp')

        # grouping by timestamp and summing up
        output = output.groupby('timestamp').sum()

        # getting the timestamps and adding them to the list
        output['timestamp'] = output.index.tolist()

        # pruning the dataset
        output = output.loc[:, ['timestamp'] + step_layout]

        # returning it
        return output

    @overrides
    def help(self) -> str:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return """
            The :class:`ProgressThroughTimeVisualization` requires a
            dataframe to have these columns:
            - `timestamp`: including the date level `str` values in "yyyy-mm-dd"
            format.
            - `step_type`: the step type column in which each row's value belongs to ["toe", "normal", "flat"]
            - `number_of_steps`: This column signifies the number of steps attributed to this category in that time.
            Note that it is easily possible to have multiple many recordings in any dates, dates have no
            uniqueness constraint.
        """

    @overrides
    def visualization_information(self) -> Dict[str, Any]:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return {
            "js": "js/visualizations/progressThroughTime.js",
            "html": "visualizations/_progress_through_time.html",
            "cache": "warehouse/visualizations/progress_through_time.csv",
            "name": "progress_through_time",
            "description": """
                This visualization assists the user by providing an efficient way to look into the shoe data.
                The viewer, having selected this scheme, chooses a resolution and then proceeds by selecting
                a start date and end date. This visualization assumes that after the selected routines are
                executed and now the "progress_through_time.csv" has been saved, in which we have
                columns for "timestamp, toe, flat, normal" to mark the timestamps and the types of walking (their counts).
                The :class:`ProgressThroughTimeVisualization` contains methodologies for quantizing the data
                and aggregating the information according to viewer's defined specifications and output the data.
                The final observation, being a completely interactive d3.js based visualization, walks the
                viewer through all the steps.
            """
        }


class ProgressThroughTimeCircularVisualization(VisualizationBase):
    """
    The :class:`ProgressThroughTimeCircularVisualization` provides a novel way of visualizing the smart shoe data.
    This visualizaton will be focused by a circular progress demonstration showing different types of walking.
    """

    def __init__(self,
                 subject: str,
                 start_date,
                 end_date,
                 scheme,
                 resolution):
        """
        The constructor method of :class:`ProgressThroughTimeVisualization`

        Parameters
        ----------
        subject: `str`, required
            The subject id (e.g. `TW06NA`)
        start_date: `str`, required
            The start date in `yyyy-mm-dd` format
        end_date: `str`, required
            The end date in `yyyy-mm-dd` format
        scheme: `str`, required
            The visualization scheme
        resolution: `str`, required
            The choices are `day`, `month`, and `year`
        """
        super(ProgressThroughTimeCircularVisualization, self).__init__()
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date
        self.scheme = scheme
        self.resolution = resolution

    @overrides
    def check_dataframe_sanity(self, dataframe: pandas.DataFrame) -> None:
        """
        Please refer to the method's description in parent class's documentation.
        """
        columns = dataframe.columns.tolist()
        assert "timestamp" in columns
        assert "step_type" in columns
        assert "number_of_steps" in columns

    @overrides
    def visualization_specific_morphing(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Please refer to the method's description in parent class's documentation.
        """
        step_layout = [
            'toe',
            'flat',
            'normal'
        ]

        output = deepcopy(dataframe)

        def quantize_date(date: str, resolution: str):
            """
            This mini function is for date quantization

            Parameters
            ----------
            date: `str`, required
                The string of date in `yyyy-mm-dd` format
            resolution: `str`, required
                The resolution, which is either `month` or `year`

            Returns
            -----------
            This method returns the quantized month as a yyyymm instance of `float`.
            """
            date = date.replace('_', '-')
            date_parts = date.split('-')

            if resolution == 'year':
                return '-'.join(date_parts[:1])
            elif resolution == 'month':
                return '-'.join(date_parts[:2])
            elif resolution == 'day':
                return '-'.join(date_parts[:3])
            else:
                raise NotImplementedError

        output["timestamp"] = output["timestamp"].apply(
            lambda x: int(quantize_date(x, self.resolution).replace('-', '')))

        for step_type in step_layout:
            output[step_type] = output[output['step_type'] == step_type]['number_of_steps']
            output[step_type].fillna(0, inplace=True)

        output = output.sort_values(by='timestamp')
        output = output.groupby('timestamp').sum()
        output['timestamp'] = output.index.tolist()

        output = output.loc[:, ['timestamp'] + step_layout]

        return output

    @overrides
    def help(self) -> str:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return """
            The :class:`ProgressThroughTimeVisualization` requires a
            dataframe to have these columns:
            - `timestamp`: including the date level `str` values in "yyyy-mm-dd"
            format.
            - `step_type`: the step type column in which each row's value belongs to ["toe", "normal", "flat"]
            - `number_of_steps`: This column signifies the number of steps attributed to this category in that time.
            Note that it is easily possible to have multiple many recordings in any dates, dates have no
            uniqueness constraint.
        """

    @overrides
    def visualization_information(self) -> Dict[str, Any]:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return {
            "js": "js/d3/d3-scale-radial.js",
            "html": "visualizations/_progress_through_time_circular.html",
            "cache": "warehouse/visualizations/progress_through_time_circular.csv",
            "name": "progress_through_time_circular",
            "description": """
                This visualization assists the user by providing an efficient way to look into the shoe data.
                The viewer, having selected this scheme, chooses a resolution and then proceeds by selecting
                a start date and end date. This visualization assumes that after the selected routines are
                executed and now the "progress_through_time_circular.csv" has been saved, in which we have
                columns for "timestamp, toe, flat, normal" to mark the timestamps and the types of walking (their counts).
                The :class:`ProgressThroughTimeCircularVisualization` contains methodologies for quantizing the data
                and aggregating the information according to viewer's defined specifications and output the data.
                The final observation, being a completely interactive D3.js based visualization, walks the
                viewer through all the steps.
            """
        }


class WalkingPieChartDuringDateRange(VisualizationBase):
    """
    The :class:`WalkingPieChartDuringDateRange` is mainly for a Pie-Chart based aggregate statistical
    visualization of our data.
    """

    def __init__(self,
                 subject: str,
                 start_date,
                 end_date,
                 scheme,
                 resolution):
        """
        Please refer to the method's description in parent class's documentation.
        """
        super(WalkingPieChartDuringDateRange, self).__init__()
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date
        self.scheme = scheme
        self.resolution = resolution

    @overrides
    def check_dataframe_sanity(self, dataframe: pandas.DataFrame) -> None:
        """
        Please refer to the method's description in parent class's documentation.
        """
        columns = dataframe.columns.tolist()
        assert "timestamp" in columns
        assert "step_type" in columns
        assert "number_of_steps" in columns

    @overrides
    def visualization_specific_morphing(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        """
        Please refer to the method's description in parent class's documentation.
        """

        # preparing the output dataframe's core data storage as a dictionary.
        output = dict()

        # preparing the step layout
        step_layout = [
            'toe',
            'flat',
            'normal'
        ]

        # this step_layout will be used in the html as well, so let's make it class variable
        self.step_layout = step_layout

        # filling the information by summing up all of the step counts during the entire time
        # selected by the user.
        for step_type in step_layout:
            output[step_type] = [
                numpy.sum(dataframe[dataframe['step_type'] == step_type]['number_of_steps'].to_numpy())]

        # forming the dataframe by that dictionary
        output = pandas.DataFrame(output)

        return output

    @overrides
    def help(self) -> str:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return """
            The :class:`WalkingPieChartDuringDateRange` requires a
            dataframe to have a column with one value for each one of the step types.
            The value indicates the number of steps in that step type during the
            selected time-range.
        """

    @overrides
    def visualization_information(self) -> Dict[str, Any]:
        """
        Please refer to the method's description in parent class's documentation.
        """
        return {
            "js": "js/d3/d3-scale-chromatic.v1.min.js",
            "html": "visualizations/_walking_chart_during_date_range.html",
            "cache": "warehouse/visualizations/walking_chart_during_date_range.csv",
            "name": "walking_chart_during_date_range",
            "description": """
                This visualization assists the user by providing an efficient way to look into the shoe data.
                The viewer, having selected this scheme, chooses a resolution and then proceeds by selecting
                a start date and end date. This visualization assumes that after the selected routines are
                executed and now the "progress_through_time.csv" has been saved, in which we have
                columns for "timestamp, toe, flat, normal" to mark the timestamps and the types of walking (their counts).

                The :class:`WalkingPieChartDuringDateRange` contains methodologies for aggregating and
                summing up all of the step counts that a subject has and compare them against each other
                in a pie-chart.
            """
        }


class WordCloudsVisualization(VisualizationBase):
    """
    The :class:`WordCloudsVisualization` is mainly responsible for the visualizations of the palette using
    word cloud pipelines.
    """
    def __init__(self, guide):
        super(WordCloudsVisualization, self).__init__(guide=guide)

    @overrides
    def check_dataframe_sanity(self, dataframe: pandas.DataFrame) -> None:
        columns = dataframe.columns.tolist()
        assert ("COMMENT" in columns) or ("PatientComment" in columns)

    @overrides
    def visualization_specific_morphing(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        return dataframe

    @overrides
    def help(self) -> str:
        return """
            The RatingTrajectoriesVisualization class requires a
            dataframe to have these three columns:
            - `timestamp`: including the date level `str` values in "yyyy-mm-dd"
            formats
            - `rating`: the rating column which includes multiple values
        """

    @overrides
    def visualization_information(self) -> Dict[str, Any]:
        return {
            "js": "js/visualizations/wordClouds.js",
            "html": "visualizations/_word_clouds.html",
            "cache": "warehouse/visualizations/word_clouds.csv",
            "name": "word_clouds",
            "description": """
                The word cloud visualization to demonstrate the importance of words by demonstrating
                their frequency of occurrence in terms of proportional magnitudes. Visualizations as such,
                if taken into account cautiously to avoid misleading interpretations, are of immense
                importance.
            """
        }

    def generate_word_cloud_picture(self, dataframe: pandas.DataFrame):
        """
        The function to generate and save the word cloud picture.

        Parameters
        ----------
        dataframe: `pandas.DataFrame`, required
            The input dataframe
        """
        if "PatientComment" in dataframe.columns.tolist():
            comment_column = "PatientComment"
        elif "COMMENT" in dataframe.columns.tolist():
            comment_column = "COMMENT"
        else:
            raise Exception("Please double check the dataframe to make sure comment column exists in it.")

        full_text = " ".join([e for e in dataframe[comment_column].tolist() if type(e) == str])


        the_coloring = numpy.array(Image.open(os.path.join(application_directory, "static/warehouse/word_clouds/bruin.png")))
        stopwords = set(STOPWORDS)
        stopwords.add("said")

        wc = WordCloud(background_color="white", max_words=2000, mask=the_coloring,
                       stopwords=stopwords, max_font_size=40, random_state=42)
        # generate word cloud
        wc.generate(full_text)

        # create coloring from image
        image_colors = ImageColorGenerator(the_coloring)

        the_cloud = wc.recolor(color_func=image_colors)

        the_cloud.to_file(os.path.join(application_directory, "static/warehouse/word_clouds/wc.png"))