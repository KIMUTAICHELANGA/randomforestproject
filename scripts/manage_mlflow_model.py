import os 
import sys
import yaml
import logging
import argepase

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model_deploy.utils import manage_mlflow_model

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    #config
    with open(args.config, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    #instantiate mlflow model
        
    logging.info('Managing mlflow model')
    mlflow_model = manage_mlflow_model(config)

    if args.prepare_model:
        logging.info('Preparing model')
        mlflow_model.prepare_model()

    if args.transition_staging:
        mflow_handler.transition_model_stage('Staging')

    if args.transition_production:
        mflow_handler.transition_model_stage('Production')