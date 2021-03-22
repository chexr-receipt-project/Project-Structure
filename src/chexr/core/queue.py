import boto3
from botocore.config import Config
from .config import settings

aws_config = Config(region_name=settings.AWS_REGION)

sqs = boto3.client("sqs", config=aws_config)


def send_message(queue_name, body, attributes={}) -> str:
    return sqs.send_message(
        QueueUrl=queue_name,
        MessageAttributes=attributes,
        MessageBody=body
    )
