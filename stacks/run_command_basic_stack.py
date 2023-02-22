from aws_cdk import Stack
from constructs import Construct
from constructors.run_command_basic import functions
from constructors.ec2 import vpc
from constructors.ec2 import ec2


class RunCommandBasicStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # AWS Lambda function

        run_command_function = functions.FunctionConstructors(self, 'RunCommandFunction')
