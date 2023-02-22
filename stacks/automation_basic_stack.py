from aws_cdk import Stack
from constructs import Construct
from constructors.Automation import ssm
from constructors.Automation import functions


class AutomationRunBookBasicStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --------------------------------------------------
        # AWS SSM Automation Document

        automation_run_book = ssm.SsmConstructors(self, 'AutomationRunBook')
        book_name = automation_run_book.book_name

        # --------------------------------------------------
        # AWS Lambda function

        prop = {
            'automation_run_book_name': book_name
        }
        ssm_automation_function = functions.FunctionConstructors(self,
                                                                 'SsmAutomationConstructor',
                                                                 **prop)
