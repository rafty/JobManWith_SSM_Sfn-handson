import aws_cdk as core
import aws_cdk.assertions as assertions

from job_man_with_ssm_sfn_handson.job_man_with_ssm_sfn_handson_stack import JobManWithSsmSfnHandsonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in job_man_with_ssm_sfn_handson/job_man_with_ssm_sfn_handson_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = JobManWithSsmSfnHandsonStack(app, "job-man-with-ssm-sfn-handson")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
