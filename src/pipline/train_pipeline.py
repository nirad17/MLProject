import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException

class TrainPipeline:
    def __init__(self) -> None:
        pass

    def initiate_training(self):
        try:
            obj = DataIngestion()
            train_set, test_set = obj.initiate_data_ingestion()

            data_transformation = DataTransformation()
            train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_set,test_set)

            model_trainer= ModelTrainer()
            return model_trainer.initiate_model_trainer(train_array=train_arr, test_array=test_arr)
        except Exception as e:
            raise CustomException(e,sys)