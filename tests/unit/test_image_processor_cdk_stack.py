import aws_cdk as core
import aws_cdk.assertions as assertions

from image_processor_cdk.image_processor_cdk_stack import ImageProcessorCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in image_processor_cdk/image_processor_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ImageProcessorCdkStack(app, "image-processor-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
