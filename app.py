#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks import vpc_stack
from stacks import run_command_basic_stack
from stacks import automation_basic_stack
from stacks import automation_2_stack
from stacks import stepfunctions_stack
from stacks import stepfunctions_stack_2


env = cdk.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)


app = cdk.App()

vpc_stack.HandsonVpc(app, 'HandsonVpcStack', env=env)

run_command_basic_stack.RunCommandBasicStack(app, "RunCommandBasicStack", env=env)

automation_basic_stack.AutomationRunBookBasicStack(app, 'AutomationRunBookStack', env=env)

automation_2_stack.AutomationRunBookStack(app, 'AutomationRunBook2Stack', env=env)

stepfunctions_stack.StepfunctionsStack(app, 'StepfunctionsStack', env=env)

stepfunctions_stack_2.StepfunctionsStack(app, 'StepfunctionsStack2', env=env)


app.synth()
