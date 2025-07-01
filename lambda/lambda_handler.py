import os
import boto3
from PIL import Image
import io
import time

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
DEST_BUCKET = os.environ["DEST_BUCKET"]
TABLE_NAME = os.environ["TABLE_NAME"]
sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]

def main(event, context):
    table = dynamodb.Table(TABLE_NAME)
    
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Download original image from S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        img = Image.open(io.BytesIO(obj["Body"].read()))

        # Create thumbnail
        img.thumbnail((128, 128))
        buf = io.BytesIO()
        img.save(buf, "JPEG")
        buf.seek(0)
        thumb_key = f"thumbnails/thumb-{os.path.basename(key)}"

        # Upload thumbnail to dest bucket
        s3.put_object(Bucket=DEST_BUCKET, Key=thumb_key, Body=buf)

        # Store metadata in DynamoDB
        table.put_item(
            Item={
                "ImageKey": key,
                "ThumbKey": thumb_key,
                "UploadedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        )

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="New Image Processed",
            Message=(
                f"A new image has been processed!\n\n"
                f"Original Image: {key}\n"
                f"Thumbnail: {thumb_key}\n"
                f"Upload Time: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"
            ),
        )
