import pickle

import numpy as np
import pandas as pd

from typing import Tuple, Union, List

import xgboost
from fastapi import HTTPException
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from challenge.settings import Settings
from challenge.utils.preprocessor import Preprocessor

settings = Settings()


class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self.preprocessor = Preprocessor()
        self.top_10_features = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        self._threshold_in_minutes = settings.DELAY_THRESHOLD

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """

        try:
            if 'Fecha-I' in data and 'Fecha-O' in data:
                data['period_day'] = data['Fecha-I'].apply(self.preprocessor.get_period_day)
                data['high_season'] = data['Fecha-I'].apply(self.preprocessor.is_high_season)
                data['min_diff'] = data.apply(self.preprocessor.get_min_diff, axis=1)
                data['delay'] = np.where(data['min_diff'] > self._threshold_in_minutes, 1, 0)

            features = pd.concat([
                pd.get_dummies(data['OPERA'], prefix='OPERA'),
                pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
                pd.get_dummies(data['MES'], prefix='MES')],
                axis=1
            )

        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")

        if target_column:
            target = data[target_column]
            return features[self.top_10_features], target.to_frame()

        features = features.reindex(columns=self.top_10_features, fill_value=0)

        return features[self.top_10_features]

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> Tuple[Union[str, dict], LogisticRegression]:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """

        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

        scale = len(y_train[y_train.delay == 0]) / len(y_train[y_train.delay == 1])
        model = xgboost.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale)

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        self.load_model(model)

        return classification_report(y_test, y_pred, output_dict=True), model

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """

        if self._model is None:
            with open("./models/model.pkl", "rb") as saved_model:
                model = pickle.load(saved_model)
                self._model = model

        predictions = np.array(self._model.predict(features))

        return predictions.tolist()

    def load_model(self, model):
        self._model = model
