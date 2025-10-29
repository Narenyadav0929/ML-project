import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from pathlib import Path

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













#             os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
#             df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
#             print('hi')
#             logging.info("Train test split iniciated")
#             train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)
#             train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
#             test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

#             logging.info("Ingestion of data is completed")

#             return (
#                 self.ingestion_config.train_data_path,
#                 self.ingestion_config.test_data_path
#             )

            
#         except Exception as e:
#             raise CustomException(e,sys)


# if __name__=="__main__":
#     obj=DataIngestion()
#     train_data,test_data=obj.initiate_data_ingestion()




