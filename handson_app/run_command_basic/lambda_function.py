import os
import time
import boto3
from aws_lambda_powertools import Logger
from aws_xray_sdk import core as x_ray

logger = Logger()
x_ray.patch_all()

SSM_OUTPUT_BUCKET_NAME = os.environ.get('SSM_OUTPUT_BUCKET_NAME')  # AWS Lambda Environment Variable

logger.info({'SSM_OUTPUT_BUCKET_NAME': SSM_OUTPUT_BUCKET_NAME})

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')


def select_ec2_instance() -> list:
    resp = ec2.describe_instances(
        Filters=[{
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }])

    logger.info({
        'function': 'ec2.describe_instances()',
        'resp:': resp})

    instances = [instance['InstanceId']
                 for reservation in resp['Reservations']
                 for instance in reservation['Instances']]
    return instances


def run_commands(instances):

    # commands = [
    #     'date +"%T.%N"',
    #     "echo %s > /tmp/from_lambda.log" % instances[0],
    #     "date",
    #     "pwd",
    #     "ls",
    #     # "ls -al",
    #     'date +"%T.%N"',
    # ]

    commands = [
        'echo --- yum update ---',
        'sudo yum -y update',
        'echo --- curl google ---',
        'curl https://www.google.com/',
    ]

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command
    # https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/sysman-rc-setting-up-cwlogs.html
    response = ssm.send_command(
        InstanceIds=instances,  # InstanceIds or Targets
        # Targets=[                 # Tag指定されたInstanceにRunCommandを実行
        #     {
        #         'Key': 'tag:env',
        #         'Values': [
        #             'handson',
        #         ]
        #     }
        # ],
        DocumentName='AWS-RunShellScript',
        Parameters={
            'workingDirectory': ['/usr/bin'],  # default work directory: /usr/bin
            'commands': commands,
            'executionTimeout': ['7200'],
        },
        OutputS3BucketName=SSM_OUTPUT_BUCKET_NAME,
        OutputS3KeyPrefix='run-shell',
        CloudWatchOutputConfig={
            # 'CloudWatchLogGroupName': 'aws/ssm/AWS-RunShellScript'   # default
            # log: command_id/instance_id/aws-runShellScript/stdout or /stderr
            'CloudWatchOutputEnabled': True
        }
    )

    logger.info({'function': 'ssm.send_command', 'response:': response})

    if not len(response['Command']['InstanceIds']):
        # Todo: Targetsでsend_command()するとInstanceIdが返らない。
        logger.info({'function': "exit() no instances in ['Command']['InstanceIds']"})
        return

    time.sleep(10)

    command_id = response['Command']['CommandId']
    for instance_id in response['Command']['InstanceIds']:
        # Todo: get_command_invocation()
        #  : StandardOutputContentにoutputがかえる

        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
        logger.info({'function': 'get_command_invocation()', 'output:': output})
        # Todo: list_command_invocations()
        #  : StandardOutputUrlにs3のurl
        # output = ssm.list_command_invocations(
        #     CommandId=command_id, InstanceId=instance_id
        # )
        # logger.info({'function': 'list_command_invocations()', 'output:': output})


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    logger.info({'function': 'lambda_handler()'})

    try:
        instances = select_ec2_instance()

        if not len(instances):  # no instance
            return
        logger.info({'function': 'select_ec2_instance()', 'instances:': instances})

        run_commands(instances=instances)
        return

    except Exception as e:
        logger.error(e)
        raise e
