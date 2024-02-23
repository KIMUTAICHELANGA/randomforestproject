import sagemaker
from src.model_build.jobs import jobs
from sagemaker.imputs import TrainingInput
from sagemake.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.parameters import ParameterString


def get_pipeline(iam_role,cfg):
        
        # Define the parameters
        input_data = ParameterString(name='InputData')
        model_approval_status = ParameterString(name='ModelApprovalStatus', default_value='PendingManualApproval')
        
        # Define the processing step
        processing_step = ProcessingStep(
            name='Processing',
            processor=get_processor(iam_role,cfg),
            inputs=[TrainingInput(input_data, '/opt/ml/processing/input')],
            outputs=[ProcessingOutput(output_name='train', source='/opt/ml/processing/train'),
                    ProcessingOutput(output_name='test', source='/opt/ml/processing/test')],
            code='src/model_build/data_preperation/prepare.py'
        )
        
        # Define the training step
        training_step = TrainingStep(
            name='Training',
            estimator=get_estimator(iam_role,cfg),
            inputs={
                'train': TrainingInput(processing_step.properties.ProcessingOutputConfig.Outputs['train'].S3Output.S3Uri, content_type='text/csv'),
                'test': TrainingInput(processing_step.properties.ProcessingOutputConfig.Outputs['test'].S3Output.S3Uri, content_type='text/csv')
            },
            code='src/model_build/training/train.py'
        )
        
        # Define the pipeline
        pipeline = Pipeline(
            name='ModelPipeline',
            parameters=[input_data, model_approval_status],
            steps=[processing_step, training_step]
        )
        
        return pipeline
