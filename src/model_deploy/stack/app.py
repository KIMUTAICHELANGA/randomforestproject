import os
import yaml
import boto3
import sagemaker
from constructs import Construct

from aws_cdk import(
    Stack,
    App,
    Duration,
    CfnOutput
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_sagemaker as sagemaker_,
    aws_apigateway as apigw,
)

def get_model_location_from_ssm():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name='model_location')
    return response['Parameter']['Value']


class InferenceStack(Stack) :

    def__init__(self, scope: Construct, id: str, **kwargs) -> None:
             super().__init__(scope, id, **kwargs)


             #Iam role for lambda

              iam_role = sagemaker.get_execution_role()

              #Read configuration

                with open('config.yaml') as file:
                    config = yaml.load(file, Loader=yaml.FullLoader)

                sagemaker_model_name = config['sagemaker_model_name']

                model_s3_location = get_model_location_from_ssm(
                    config['model_s3_location_ssm_parameter_name']
                )


                container = sagemaker_CfnModel.ContainerDefinitionProperty(
                    image=config['model_image'],
                    modelDataUrl=model_s3_location,
                    environment={
                        "MLFLOW_DEPLOYMENT_FLAVOR_NAME:"
                        "SERVING_ENVIRONMENT_NAME": "local",
                    },
                )
                 

                 sage_maker_model = sagemaker.CfnModel(
                        self,
                        "SagemakerModel",
                        execution_role_arn=iam_role.role_arn,
                        primary_container=container,
                        model_name=sagemaker_model_name,
                    )

                    production_variants = sage_maker.CfnEndpointConfig.ProductionVariantProperty(
                        modelName=sage_maker_model.ref,
                        variantName="prod",
                        initialInstanceCount=1,
                        initialVariantWeight=1.0,
                        instanceType=config['instance_type'],
                    )

                    sagemaker_endpoint_config = sagemaker.CfnEndpointConfig(
                        self,
                        "SagemakerEndpointConfig",
                        production_variants=[production_variants],
                        endpoint_config_name=sagemaker_model_name,
                    )

                    sagemaker_endpoint = sagemaker.CfnEndpoint(
                        self,
                        "SagemakerEndpoint",
                        endpoint_config_name=sagemaker_endpoint_config.ref,
                        endpoint_name=sagemaker_model_name,
                    )

                    role= iam.Role.from_role_arn(
                        self,
                        "Role",
                        role_arn=iam_role.role_arn,
                        function_name="LambdaFunction",
                        code= lambda_.Code.from_asset("lambda"),
                        handler="handler.handler",
                        runtime=lambda_.Runtime.PYTHON_3_8,
                        memory_size=128,
                        timeout=Duration.seconds(30),
                        environment={"ENDPOINT_NAME": sagemaker_endpoint.ref},

                    )

                    api = apigw.LambdaRestApi(
                        self,
                        "Endpoint",
                        handler=handler,
                        proxy=False,
                    )
                    

                    CfnOutput(
                        self,
                        "ApiUrl",
                        value=api.url,
                    )

                    app = App()
                    InferenceStack(app, "InferenceStack")
                    app.synth()