#!/usr/bin/env python3
import aws_cdk as cdk

from image_processor_cdk.image_processor_cdk_stack import ImageProcessorCdkStack
from image_processor_cdk.config import load_config

config = load_config()


app = cdk.App()
ImageProcessorCdkStack(app, "ImageProcessorCdkStack", config=config)
app.synth()
