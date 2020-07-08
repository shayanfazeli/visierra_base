from typing import List, Any, Tuple
import os
import pandas
import numpy
from copy import deepcopy
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from plauthor.plotters.matrix import visualize_matrix
from application import application_directory
import pickle
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def category_to_class(x: Any, category_layout: List[Any]):
    assert x in category_layout, "the provided category layout is not valid"
    return int(category_layout.index(x))


def prepare_the_dataframe_for_ml(
        input_dataframe: pandas.DataFrame,
        label_column: str,
        feature_columns: List[str]
):
    # deep copy just in case
    input_dataframe = deepcopy(input_dataframe)

    # filling all of the not a numbers
    input_dataframe.fillna(0, inplace=True)

    # filtering out features and label columns
    input_dataframe = input_dataframe.loc[:, feature_columns + [label_column]]

    # checking feature and label columns and categorizing if necessary
    for column_name in feature_columns:
        try:
            tmp_column = input_dataframe.loc[:, column_name].astype(float)
            input_dataframe.loc[:, column_name] = tmp_column
        except Exception as e:
            try:
                tmp_column = input_dataframe.loc[:, column_name].astype(str)
                tmp_layout = tmp_column.unique().tolist()
                tmp_column = tmp_column.apply(lambda x: category_to_class(x, tmp_layout))
                input_dataframe.loc[:, column_name] = tmp_column
            except Exception as e:
                Exception("Protocol failed on the dataframe, not supported dataset")

    ## for label column
    column_name = label_column
    try:
        tmp_column = input_dataframe.loc[:, column_name].astype(float)
        input_dataframe.loc[:, column_name] = tmp_column
    except Exception as e:
        try:
            tmp_column = input_dataframe.loc[:, column_name].astype(str)
            original_label_layout = tmp_column.unique().tolist()
            tmp_column = tmp_column.apply(lambda x: category_to_class(x, original_label_layout))
            input_dataframe.loc[:, column_name] = tmp_column
        except Exception as e:
            Exception("Protocol failed on the dataframe, not supported dataset")

    list_of_labels = input_dataframe.loc[:, label_column].unique().tolist()

    train_dfs = []
    test_dfs = []

    for label in list_of_labels:
        sub_dataframe = input_dataframe[input_dataframe[label_column] == label]
        assert sub_dataframe.shape[0] > 5, "not enough example is provided"
        test_example_count = int(0.2 * sub_dataframe.shape[0])
        test_dfs.append(sub_dataframe.iloc[test_example_count:, :])
        train_dfs.append(sub_dataframe.iloc[:test_example_count, :].sample(n=1000, replace=True))

    train_dataframe = shuffle(pandas.concat(train_dfs))
    test_dataframe = pandas.concat(test_dfs)

    X_train = train_dataframe.to_numpy()
    y_train = X_train[:, -1].ravel()
    X_train = X_train[:, :-1]

    X_test = test_dataframe.to_numpy()
    y_test = X_test[:, -1].ravel()
    X_test = X_test[:, :-1]

    return X_train, y_train, X_test, y_test, original_label_layout


def ffnn_experiment(
        X_train: numpy.ndarray,
        y_train: numpy.ndarray,
        X_test: numpy.ndarray,
        y_test: numpy.ndarray,
        list_of_labels: List[Any],
        hidden_layer_config: Tuple[int] = (60,2),
        perform_pca: int = 1,
        pca_dim: int = 50
):
    output_path = os.path.join(application_directory, 'static/ml_toolkit/ffnn_experiment.png')

    if os.path.isfile(output_path):
        os.system('rm ' + output_path)

    # min-max scaling
    scaler = MinMaxScaler()

    # fitting the scaler
    scaler.fit(X_train)

    # applying the scaler
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # pca
    if perform_pca == 1:
        pca = PCA(n_components=pca_dim)
        pca.fit(X_train)
        coverage = numpy.sum(pca.explained_variance_ratio_)
        X_train = pca.transform(X_train)
        X_test = pca.transform(X_test)

    classifier = MLPClassifier(
        solver='lbfgs',
        verbose=True,
        alpha=1e-5,
        hidden_layer_sizes=hidden_layer_config,
        random_state=2019,
        max_iter=1000,
        shuffle=True)

    classifier.fit(X_train, y_train.ravel())

    y_pred = classifier.predict(X_test)

    conf_mat = confusion_matrix(y_pred, y_test, numpy.arange(len(list_of_labels)).tolist())

    visualize_matrix(conf_mat, column_names=list_of_labels, row_names=list_of_labels, save_to_file=output_path, show=False, figure_size=10.0)

