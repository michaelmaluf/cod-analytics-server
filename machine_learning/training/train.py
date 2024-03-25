from io import BytesIO
from datetime import datetime

from sklearn.pipeline import Pipeline
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import make_scorer
import pandas as pd
import joblib

from machine_learning.data_preparation import fetch_data, clean_data, separate_features_and_labels, feature_engineering, \
    data_augmentation, drop_columns, scale_predictions, custom_model_evaluation, custom_evaluation_wrapper, display_features_importances
from app.enums import GameModeType
from app import create_app, db

from machine_learning.transformers import preprocessor
from machine_learning.ml_models import CODModel
import machine_learning.const as const
from app.database.models import MLModel, GameMode


def prepare_data(df):
    clean_df = clean_data(df)
    clean_fe_df = feature_engineering(clean_df)
    clean_fe_dropped_df = drop_columns(clean_fe_df)
    clean_fe_dropped_aug_df = data_augmentation(clean_fe_dropped_df)
    df_processed = clean_fe_dropped_aug_df.sort_values(by='date', ascending=True, ignore_index=True).drop('date',
                                                                                                          axis=1)

    X, y = separate_features_and_labels(df_processed)
    return X, y


def save_model_to_db(game_mode, hyperparameters, model_pipeline):
    model_buffer = BytesIO()
    joblib.dump(model_pipeline, model_buffer)
    model_bytes = model_buffer.getvalue()

    new_ml_model = MLModel(
        hyperparameters=hyperparameters,
        model_data=model_bytes
    )

    with app.app_context():
        new_ml_model.game_mode = db.session.query(GameMode).filter_by(name=game_mode).first()
        db.session.add(new_ml_model)
        db.session.commit()
        db.session.close()


def train_game_mode_model(game_mode, app):
    with app.app_context():
        game_mode_data = fetch_data(game_mode, db.session)

    X, y = prepare_data(game_mode_data)
    hyperparams = getattr(const, f'{game_mode.name}_HYPERPARAMS')
    target_score = getattr(const, f'{game_mode.name}_TARGET_SCORE')
    game_mode_model = CODModel(**hyperparams)
    game_mode_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', game_mode_model)])

    tcsv = TimeSeriesSplit(n_splits=const.TIME_SERIES_SPLITS)
    all_y_tests = []
    all_predictions = []

    for train_index, test_index in tcsv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        game_mode_pipeline.fit(X_train, y_train)

        predictions = game_mode_pipeline.predict(X_test)
        scaled_predictions = scale_predictions(predictions, target_score)

        y_test_df = y_test.reset_index(drop=True)
        scaled_predictions_df = pd.DataFrame(scaled_predictions, index=test_index, columns=['team_one_score', 'team_two_score'])

        all_y_tests.append(y_test_df)
        all_predictions.append(scaled_predictions_df)

    all_y_tests_df = pd.concat(all_y_tests, ignore_index=True)
    all_predictions_df = pd.concat(all_predictions, ignore_index=True)

    evaluation_score = custom_model_evaluation(all_y_tests_df, all_predictions_df, target_score)

    with open('stats.txt', 'a') as file:
        results = f'\n\nModel results: {datetime.now()}\n' \
                  f'Game_mode: {game_mode}\n' \
                  f'hyperparameters: {hyperparams}\n' \
                  f'Evaluation score: {evaluation_score}'
        file.write(results)

    save_model_to_db(game_mode, hyperparams, game_mode_pipeline)

    display_features_importances(game_mode_pipeline, X)


def perform_grid_search(game_mode, app):
    with app.app_context():
        game_mode_data = fetch_data(game_mode, db.session)

    X, y = prepare_data(game_mode_data)
    game_mode_model = CODModel()
    game_mode_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', game_mode_model)])

    custom_score = make_scorer(custom_evaluation_wrapper, greater_is_better=True)

    grid_search = GridSearchCV(game_mode_pipeline, const.GRIDSEARCH_PARAM_GRID, cv=TimeSeriesSplit(n_splits=5),
                               scoring=custom_score, verbose=2, n_jobs=6)

    grid_search.fit(X, y)

    best_parameters = grid_search.best_params_
    best_score = grid_search.best_score_

    with open('stats.txt', 'a') as file:
        results = f'\n\nGrid search results: {datetime.now()}\n' \
                  f'Game_mode: {game_mode}\n' \
                  f'hyperparameters: {const.GRIDSEARCH_PARAM_GRID}\n' \
                  f'Best parameters: {best_parameters}\n' \
                  f'Best score: {best_score}'
        file.write(results)


def train_all_models(app):
    train_game_mode_model(GameModeType.HARDPOINT, app)
    train_game_mode_model(GameModeType.SEARCH_AND_DESTROY, app)
    train_game_mode_model(GameModeType.CONTROL, app)


def perform_grid_search_all_models(app):
    perform_grid_search(GameModeType.HARDPOINT, app)
    perform_grid_search(GameModeType.SEARCH_AND_DESTROY, app)
    perform_grid_search(GameModeType.CONTROL, app)


if __name__ == '__main__':
    app = create_app()
    train_all_models(app)
    # perform_grid_search_all_models(app)
