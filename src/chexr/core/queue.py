import boto3
from botocore.config import Config
from .config import settings
from logging import info

aws_config = Config(region_name=settings.AWS_REGION)

sqs = boto3.client("sqs", config=aws_config)


def send_message(queue_name, body, attributes={}) -> str:
    info("Sending message [%s] to queue [%s]", body, queue_name)
    return sqs.send_message(
        QueueUrl=queue_name,
        MessageAttributes=attributes,
        MessageBody=body
    )
