import pandas
import numpy
import os, sys
from copy import deepcopy
from typing import List, Dict, Any


def apply_single_transformation(dataframe, single_transformation):
    dataframe = deepcopy(dataframe)
    if single_transformation["name"] == "limit_range":
        if single_transformation["upper_bound"][1] == 'closed':
            indices = dataframe[single_transformation["column"]] <= single_transformation["upper_bound"][0]
        else:
            indices = dataframe[single_transformation["column"]] < single_transformation["upper_bound"][0]

        if single_transformation["lower_bound"][1] == 'closed':
            indices = indices & (dataframe[single_transformation["column"]] >= single_transformation["lower_bound"][0])
        else:
            indices = indices & (dataframe[single_transformation["column"]] > single_transformation["lower_bound"][0])

        if single_transformation["negation"]:
            indices = ~indices
        dataframe = dataframe[indices]
    elif single_transformation["name"] == "equality":
        indices = dataframe[single_transformation["column"]] == single_transformation['value']
        if single_transformation['negation']:
            dataframe = dataframe[~indices]
        else:
            dataframe = dataframe[indices]

    elif single_transformation["name"] == "inequality":
        if single_transformation["type"] == '>':
            indices = dataframe[single_transformation["column"]] > single_transformation['value']
        elif single_transformation["type"] == '>=':
            indices = dataframe[single_transformation["column"]] >= single_transformation['value']
        elif single_transformation["type"] == '<':
            indices = dataframe[single_transformation["column"]] < single_transformation['value']
        elif single_transformation["type"] == '<=':
            indices = dataframe[single_transformation["column"]] <= single_transformation['value']
        else:
            return ValueError
        if single_transformation['negation']:
            dataframe = dataframe[~indices]
        else:
            dataframe = dataframe[indices]

    elif single_transformation["name"] == "random_selection":
        number_of_elements = single_transformation["row_count"]
        dataframe = dataframe.sample(number_of_elements, replace=True)
    else:
        raise ValueError

    return dataframe


def transform_dataframe(
        dataframe: pandas.DataFrame,
        guide: Dict[Any, Any]
):
    """
    The :func:`transform_dataframe` applies the transformations that the user has requested to the dataframe
    in question.

    ```
        transformations = {
            [
                {
                    "name": "limit_range",
                    "column": "x1",
                    "upper_bound": [22.2, "closed"],
                    "lower_bound": [1, "open"],
                    "negation": false
                },
                {
                    "name": "equality",
                    "column": "y",
                    "value": 1,
                    "negation": false
                },
                {
                    "name": "inequality",
                    "column": "y",
                    "type": ">"
                    "value": 2
                }
            ]
        }
    ```

    Parameters
    -----------
    dataframe: `pandas.DataFrame`, required
        This is the input dataframe. Usually, only the big dataframes are to be stored in the warehouse folder
        (note that it is not realistic to visualize HUGE datasets, so the one-file-assumption is plausible.
    guide: `Dict[str, Any]`, required
        For the first time, "guide" is going to enable the user to perform his/her own modifications and/or transformations
        to the selected dataframe. These, include transformations, a transformation is a list of transformations
        that the user has written. Each element is a dict including a "name" and a set of characteristics.
        The user can also specify a field called `column_mapping`, say for a visualization we need columns `x1`,
        x2`, and `y`, to show them.
        we will run {'x1': 'mycolumn1', 'x2': 'mycolumn2', 'y': 'c'}

    Returns
    -----------
    The output of this method is a brand new dataframe suitable for the visualization in question, along
    with a bundle of metadata which might be used in the new visualization's html file in order to show more
    useful information to the user.
    """
    output_dict = dict()
    for column in dataframe.columns.tolist():
        output_dict[column] = dataframe[column].tolist()

    if "column_mapping" in guide.keys():
        column_mapping = guide["column_mapping"]
        for column in column_mapping.keys():
            output_dict[column_mapping[column]] = dataframe[column].tolist()

    output = pandas.DataFrame(output_dict)

    if "transformations" in guide.keys():
        transformations = guide["transformations"]
        for single_transformation in transformations:
            output = apply_single_transformation(output, single_transformation)

    return output

