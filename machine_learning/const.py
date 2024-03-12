TIME_SERIES_SPLITS = 5

HARDPOINT_TARGET_SCORE = 250
SEARCH_AND_DESTROY_TARGET_SCORE = 6
CONTROL_TARGET_SCORE = 3


HARDPOINT_HYPERPARAMS = {
    'objective': 'reg:squarederror',
    'n_estimators': 100,              # Number of boosting stages
    'learning_rate': 0.1,             # Shrinkage parameter (step size)
    'max_depth': 3,                   # Maximum depth of individual trees
    'min_child_weight': 1,            # Minimum sum of instance weight needed in a child
    'subsample': 1,                   # Subsample ratio of the training instances
    'colsample_bytree': 1,            # Subsample ratio of columns when constructing each tree
    'gamma': 0,                       # Minimum loss reduction required to make a further partition on a leaf node
    'reg_alpha': 0,                   # L1 regularization term on weights
    'reg_lambda': 1,                  # L2 regularization term on weights
    'random_state': 42
}

SEARCH_AND_DESTROY_HYPERPARAMS = {
    'objective': 'reg:squarederror',
    'n_estimators': 100,              # Number of boosting stages
    'learning_rate': 0.1,             # Shrinkage parameter (step size)
    'max_depth': 3,                   # Maximum depth of individual trees
    'min_child_weight': 1,            # Minimum sum of instance weight needed in a child
    'subsample': 1,                   # Subsample ratio of the training instances
    'colsample_bytree': 1,            # Subsample ratio of columns when constructing each tree
    'gamma': 0,                       # Minimum loss reduction required to make a further partition on a leaf node
    'reg_alpha': 0,                   # L1 regularization term on weights
    'reg_lambda': 1,                  # L2 regularization term on weights
    'random_state': 42
}

CONTROL_HYPERPARAMS = {
    'objective': 'reg:squarederror',
    'n_estimators': 100,              # Number of boosting stages
    'learning_rate': 0.1,             # Shrinkage parameter (step size)
    'max_depth': 3,                   # Maximum depth of individual trees
    'min_child_weight': 1,            # Minimum sum of instance weight needed in a child
    'subsample': 1,                   # Subsample ratio of the training instances
    'colsample_bytree': 1,            # Subsample ratio of columns when constructing each tree
    'gamma': 0,                       # Minimum loss reduction required to make a further partition on a leaf node
    'reg_alpha': 0,                   # L1 regularization term on weights
    'reg_lambda': 1,                  # L2 regularization term on weights
    'random_state': 42
}

GRIDSEARCH_PARAM_GRID = {
    'model__n_estimators': [100, 200, 300],
    'model__learning_rate': [0.01, 0.1, 0.2],
    'model__max_depth': [3, 4, 5],
    # 'model__min_child_weight': [1, 2, 3],
    # 'model__subsample': [0.5, 0.8, 1.0],
    # 'model__colsample_bytree': [0.5, 0.8, 1.0],
    # 'model__gamma': [0, 0.1, 0.2],
    # 'model__reg_alpha': [0, 0.1, 1],
    # 'model__reg_lambda': [1, 2, 3],
}

# start with first three, narrow down selection from results, and continue moving downward
