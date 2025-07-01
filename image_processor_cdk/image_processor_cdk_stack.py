from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from constructs import Construct


class ImageProcessorCdkStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, config=None, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_bucket = config.get("source_bucket")
        dest_bucket = config.get("dest_bucket")
        lambda_function_name = config.get("lambda_function_name")
        dynamodb_table_name = config.get("dynamodb_table_name")
        email = config.get("email")
        topic_name = config.get("topic_name")

        # 1. Pillow Layer (ensure you have a valid zip at this path!)
        pillow_layer = _lambda.LayerVersion(
            self,
            "PillowLayer",
            code=_lambda.Code.from_asset("pillow_layer.zip"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
            description="Pillow library (for image processing)",
        )

        # 2. S3 Buckets
        self.source_bucket = s3.Bucket(
            self,
            "SourceBucket",
            bucket_name=source_bucket,
            removal_policy=RemovalPolicy.DESTROY, 
            auto_delete_objects=True,
        )

        self.dest_bucket = s3.Bucket(
            self,
            "DestBucket",
            bucket_name=dest_bucket,
            removal_policy=RemovalPolicy.DESTROY,  
            auto_delete_objects=True,
        )

        # 3. DynamoDB Table
        self.table = dynamodb.Table(
            self,
            "ImageMetaTable",
            table_name=dynamodb_table_name, 
            partition_key=dynamodb.Attribute(
                name="ImageKey", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        # 4. SNS Topic + Email Subscription
        self.topic = sns.Topic(self, "ImageProcessedTopic", topic_name=topic_name)
        self.topic.add_subscription(subs.EmailSubscription(email))

        # 5. Lambda Function
        lambda_fn = _lambda.Function(
            self,
            "ImageProcessorFunction",
            function_name=lambda_function_name,
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.main",
            code=_lambda.Code.from_asset("lambda"),
            layers=[pillow_layer],
            environment={
                "DEST_BUCKET": self.dest_bucket.bucket_name,
                "TABLE_NAME": self.table.table_name,
                "TOPIC_ARN": self.topic.topic_arn,
            },
            timeout=Duration.seconds(30),
        )

        # 6. Permissions
        self.topic.grant_publish(lambda_fn)
        self.source_bucket.grant_read(lambda_fn)
        self.dest_bucket.grant_write(lambda_fn)
        self.table.grant_write_data(lambda_fn)

        # 7. S3 event notification (only on object create)
        notification = s3n.LambdaDestination(lambda_fn)
        self.source_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, notification
        )
