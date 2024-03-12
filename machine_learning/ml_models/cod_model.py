import xgboost as xgb
from sklearn.metrics import r2_score
from sklearn.base import BaseEstimator, TransformerMixin

class CODModel(BaseEstimator, TransformerMixin):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.model = xgb.XGBRegressor(**kwargs)

    def set_params(self, **params):
        self.kwargs.update(params)
        self.model = xgb.XGBRegressor(**self.kwargs)
        return self

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        predictions = self.predict(X)
        return r2_score(y, predictions)

    @property
    def feature_importances_(self):
        return self.model.feature_importances_