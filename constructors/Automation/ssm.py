import yaml  # pip install PyYAML
from constructs import Construct
from aws_cdk import aws_ssm
from aws_cdk import Aws


class SsmConstructors(Construct):

    def __init__(self, scope: "Construct", id_: str, **kwargs: dict) -> None:
        super().__init__(scope, id_)

        # self.output_bucket_name = f'ssm-output-{Aws.ACCOUNT_ID}-{Aws.REGION}'
        self.cfn_document = self.create_automation_document()
        self.book_name = self.cfn_document.name

    def create_automation_document(self):

        with open('constructors/Automation/handson_automation_runbook.yaml', 'r') as f:
            doc_content = yaml.safe_load(f)

        cfn_document = aws_ssm.CfnDocument(self,
                                           'HandsonAutomationRunBook',
                                           document_type='Automation',
                                           document_format='YAML',
                                           name="handson_automation",
                                           update_method='NewVersion',
                                           content=doc_content)

        return cfn_document
