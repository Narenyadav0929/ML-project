
# Basic Import
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object
# preprosessing tools
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
# Modelling
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_tranning(self,train_arr,test_arr):
        try:
            logging.info("Model tranning is started")
            X_train,X_test, y_train, y_test =(
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )

            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "SVR": SVR()
                }
            
            model_report : dict = evaluate_models(X_train=X_train,X_test=X_test,y_test=y_test,y_train=y_train,models=models)
            
            # to get best model score
            best_model_score = max(sorted(list(model_report.values())))

            # to get best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model  = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException("No best model found")

            logging.info(f"The best model name is {best_model_name} and score is {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            best_model.fit(X_train,y_train)
            predicted = best_model.predict(X_test)
            score = r2_score(y_test,predicted)
            return score




            





        except Exception as e:
            raise CustomException(e,sys)