import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from pathlib import Path
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

@dataclass
class DataIngestionConfig():
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """Read the raw dataset, persist it, and create train/test splits."""
        logging.info("Entered the data ingestion method or component")
        try:
             # Make the CSV path safe & clear
            data_path = os.path.join('notebook', 'data', 'stud.csv')
            df = pd.read_csv(data_path)
            os.makedirs('artifacts', exist_ok=True)
            logging.info('Read the dataset as dataframe')
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True,
            )
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformer = DataTransformation()
    train_arr,test_arr,_ =data_transformer.initiate_data_transformation(train_data,test_data)

    model_trainner = ModelTrainer()
    score = model_trainner.initiate_model_tranning(train_arr=train_arr,test_arr=test_arr)
    print(score)











