import os
import sys
import yaml
import logging
import sagemaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model_build import jobs

# Set up logging
logging.basicConfig(level=logging.INFO)

if__name__ == '__main__':

#iam role

iam_role = sagemaker.get_execution_role()

#config

with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

#run processing jobs
    
logging.info('Running processing jobs')
processor = jobs.Processor(config, iam_role)
processor.run_jobs(
    code = config['processing']['code'],
    output = [
        sagemaker.processing.ProcessingOutput(
            source = config['processing']['output'],
    ]
)

# get training input from processing'

processing_job_name = processor.jobs[-1].describe()['ProcessingJobName']
training_input = processor.get_output(processing_job_name, 'output')
logging.info(f'Training input: {training_input}')

#run training jobs
logging.info("run training job")
estimator = jobs.Estimator(config, iam_role)
estimator.fit(training_input)