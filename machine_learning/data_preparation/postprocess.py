import numpy as np
import pandas as pd


def scale_predictions(predictions, target_score):
    """
    Adjusts the predictions so that the winning team's score is always 250.
    """
    adjusted_predictions = predictions.copy()
    for i in range(len(predictions)):
        winning_index = np.argmax(predictions[i])
        losing_index = 1 - winning_index
        multiplier = target_score / adjusted_predictions[i, winning_index]
        adjusted_predictions[i, winning_index] = target_score
        adjusted_predictions[i, losing_index] = adjusted_predictions[i, losing_index] * multiplier
    return adjusted_predictions


def custom_model_evaluation(y_true, y_pred, target_score, winner_weight=0.7, score_weight=0.3):
    # Determine winners based on a score of 250, 1 if team_one wins, 0 if team_two wins
    winner_true = (y_true['team_one_score'] > y_true['team_two_score']).astype(int)
    winner_pred = (y_pred['team_one_score'] > y_pred['team_two_score']).astype(int)

    # Calculate winner accuracy
    correct_winner = (winner_true == winner_pred).astype(int)
    winner_accuracy = correct_winner.mean()

    # Calculate score differences and accuracy (you might adapt this depending on how you want to handle score prediction accuracy)
    score_diff = np.abs(y_true - y_pred).to_numpy().mean()

    # Combine the metrics
    custom_score = winner_weight * winner_accuracy + score_weight * (
            1 - (score_diff * 1.25) / target_score)  # Normalize score difference

    return custom_score


def custom_evaluation_wrapper(y_true, y_pred):
    if (y_true > 200).any(axis=1).any():
        target_score = 250
    elif (y_true > 4).any(axis=1).any():
        target_score = 6
    else:
        target_score = 3

    scaled_predictions = scale_predictions(y_pred, target_score)
    y_pred_df = pd.DataFrame(scaled_predictions, index=y_true.index, columns=['team_one_score', 'team_two_score'])

    score = custom_model_evaluation(y_true, y_pred_df, target_score)
    return score


def get_feature_names(column_transformer):
    output_features = []

    for name, pipe, features in column_transformer.transformers_:
        if name != 'remainder':
            for i in pipe.get_feature_names_out(features):
                output_features.append(i)
        else:
            output_features.extend(features)

    return output_features


def display_features_importances(pipeline, X):
    model = pipeline.named_steps['model']
    feature_importances = model.feature_importances_

    feature_names = X.columns

    feature_names_after_preprocessing = get_feature_names(pipeline.named_steps['preprocessor'])

    if len(feature_names_after_preprocessing) == len(feature_importances):
        importance_dict = dict(zip(feature_names, feature_importances))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        for feature, importance in sorted_importance:
            print(f"{feature}: {importance}")
    else:
        print("The number of features after preprocessing does not match the original number.")