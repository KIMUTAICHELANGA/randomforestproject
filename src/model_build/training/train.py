import os
import logging
import argparse
import pandas as pd
from sklearn import ensemble
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn

logging.basicConfig(level=logging.INFO)


def train(args):
    # Set MLflow server
    mlflow.set_tracking_uri(args.mlflow_uri)
    
    # Load data
    logging.info("Loading data...")
    data = pd.read_csv(args.data_path)
    hyperparameters = json.load(args.hyperparameters)

    # Split data into train and test sets
    logging.info("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns !=hyperparameters ['target']],
    df[hyperparameters["target"]] ,test_size=0.2, random_state=42)
    
    # Initialize and train the model
    logging.info("Training the model...")
    model = ensemble.RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth)
    model.fit(X_train, y_train)
    
    # Log the model parameters and metrics to MLflow
    with mlflow.start_run():
        logging.info("Logging model parameters and metrics to MLflow...")
        mlflow.log_params({
            'n_estimators': args.n_estimators,
            'max_depth': args.max_depth
        })
        
        mlflow.log_metrics({
            'train_accuracy': model.score(X_train, y_train),
            'test_accuracy': model.score(X_test, y_test)
        })
        
        # Save the trained model
        logging.info("Saving the trained model...")
        mlflow.sklearn.log_model(model, 'model')
        
        # Print the model's feature importances
        logging.info("Printing the model's feature importances...")
        feature_importances = pd.Series(model.feature_importances_, index=X.columns)
        print('Feature Importances:')
        print(feature_importances)