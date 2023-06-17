import os
import sys
from src.exception import CustomException
from src.logger import logging

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer # datasets containing hetrogenous data types 
#since we may want to scale the numeric features (or mean impute ) and one-hot encode the categorical ones.

import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTranformationConfig:
    preprocessor_obj_file :str = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation() :
    def __init__(self):
        self.data_transformation_config = DataTranformationConfig()

    def get_data_transformation_obj(self): #returns transformed columns(both num and cat) obj
        try:
            num_features = ['reading_score', 'writing_score']
            cat_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            #Numerical Pipeline
            num_pipeline = Pipeline(
                [
                    ("impute",SimpleImputer(strategy="median")),
                    ('scaler', StandardScaler())
                ]
            )

            #Categorical Pipeline
            cat_pipeline = Pipeline(
                [
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Categorical Features: {cat_features}")
            logging.info(f"Numerical Features: {num_features}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline,num_features),
                    ("cat_pipeline", cat_pipeline,cat_features)
                ]
            )
            logging.info("Returning Preprocessing obj")
            return preprocessor

        except Exception as e:
            CustomException(e,sys)

    def initiate_data_transformation(self, train_path, test_path): #returns trandformed train_arr, test_arr and pkl_file_path
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading of train and test dataframe completed")

            logging.info("Obtaining Preprocessing Object")

            preprocessing_obj = self.get_data_transformation_obj()
            logging.info("Got Preprocessing obj")
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_features_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_features_train_df = train_df[target_column_name]

            input_features_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_features_test_df = test_df[target_column_name]

            logging.info("Applying Preprocessing object on training and test data frame")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_features_test_df)

            logging.info("Preprocessing done")

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_features_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_features_test_df)]


            logging.info("Saved preprocessor obj")

            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file,
                obj= preprocessing_obj
            )

            return(train_arr,test_arr, self.data_transformation_config.preprocessor_obj_file)
        except Exception as e:
            # CustomException(e,sys)
            print(e)
