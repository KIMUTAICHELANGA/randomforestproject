

def get_estimator(iam_role,cfg):

    estimator = ContainerEstimator(
        role=iam_role,
        instance_count=cfg['instance_count'],
        instance_type=cfg['instance_type'],
        image_uri=cfg['image_uri'],
        output_path=cfg['output_path'],
        sagemaker_session=cfg['sagemaker_session']
    )
    
    return estimator

def get_processor(iam_role,cfg):
    
    processor  = ScriptProcessor(

        role =iam_role,
        image_uri = cfg['image_uri'],
        command = cfg['command'],
        instance_count = cfg['instance_count'],
        instance_type = cfg['instance_type'],
        command = cfg['command'],
        env = cfg['env'],
        base_job_name = cfg['base_job_name'],
    )


    return processor