import boto3
import json
import time
from datetime import datetime

LOG_GROUP = "/securityhub/all-findings"  # Create manually or allow Lambda to create
REGION = "us-east-1"  # Change to your region

child_accounts = [
    {'account_id': '<child account>', 'role_name': 'SecurityHubReadRole'}
]

def assume_role(account_id, role_name):
    sts = boto3.client('sts')
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    response = sts.assume_role(RoleArn=role_arn, RoleSessionName="SecurityHubSession")
    return response['Credentials']

def log_to_cloudwatch(log_client, stream_name, message):
    MAX_LOG_SIZE = 1024 * 1024  # 1 MB

    try:
        log_client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=stream_name)
    except log_client.exceptions.ResourceAlreadyExistsException:
        pass

    seq_token = None
    try:
        response = log_client.describe_log_streams(logGroupName=LOG_GROUP, logStreamNamePrefix=stream_name)
        streams = response['logStreams']
        if streams and 'uploadSequenceToken' in streams[0]:
            seq_token = streams[0]['uploadSequenceToken']
    except Exception:
        pass

    # Split message into chunks
    chunks = [message[i:i + MAX_LOG_SIZE - 1000] for i in range(0, len(message), MAX_LOG_SIZE - 1000)]

    for chunk in chunks:
        log_event = {
            'logGroupName': LOG_GROUP,
            'logStreamName': stream_name,
            'logEvents': [{
                'timestamp': int(time.time() * 1000),
                'message': chunk
            }]
        }

        if seq_token:
            log_event['sequenceToken'] = seq_token

        response = log_client.put_log_events(**log_event)
        seq_token = response.get('nextSequenceToken')

def lambda_handler(event, context):
    logs = boto3.client('logs', region_name=REGION)

    # Ensure the log group exists
    try:
        logs.create_log_group(logGroupName=LOG_GROUP)
    except logs.exceptions.ResourceAlreadyExistsException:
        pass

    for account in child_accounts:
        creds = assume_role(account['account_id'], account['role_name'])
        sh_client = boto3.client('securityhub',
            region_name=REGION,
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken']
        )

        findings = []
        paginator = sh_client.get_paginator('get_findings')
        for page in paginator.paginate():
            findings.extend(page['Findings'])

        log_message = json.dumps({
            'account_id': account['account_id'],
            'timestamp': datetime.utcnow().isoformat(),
            'findings': findings
        }, default=str)

        log_to_cloudwatch(logs, stream_name=account['account_id'], message=log_message)
