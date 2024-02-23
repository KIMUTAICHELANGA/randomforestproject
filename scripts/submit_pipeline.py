import os
import sys
import yaml
import logging
import sagemaker
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model_build.pipeline import get_pipeline

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    #iam role
    iam_role = sagemaker.get_execution_role()

    #config
    with open(args.config, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    #instatiate of pipeline
        
    logging.info('Running pipeline')
    pipeline = get_pipeline(config, iam_role)

    # create/update the pipeline

    logging.info('Creating/updating the pipeline')
    pipeline.upsert()

    if args.run_execution:
        logging.info('Starting pipeline execution')
        
        pipeline.start_execution()

