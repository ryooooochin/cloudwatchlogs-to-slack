import json
import logging
import os
import datetime
import slackweb
import boto3
import re
import gzip
from base64 import b64decode
from datetime import datetime
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_TBL'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    log_data = event['awslogs']['data']
    decoded_data = b64decode(log_data)
    json_data = json.loads(gzip.decompress(decoded_data))
    log_group = str(json_data['logGroup'])
    log_stream = str(json_data['logStream'])
    timestamp = 0
    messages = []
    
    item = get_item(log_group)
    if not item:
        logger.info("No item found for %s", log_group)
        return
    
    # slackの設定
    HOOK_URL = item['webhookurl']
    slack = slackweb.Slack(url=HOOK_URL)

    exclude_regex = item['exclude']
    for logevent in json_data['logEvents']:
        found_in_rule = False
        tmp_message = str(logevent['message'])
        if exclude_regex is not None:
            for rule in exclude_regex:
                logger.info("log_message: %s", tmp_message)
                logger.info("rule: %s", rule['exp'])
                if re.search(rule['exp'], tmp_message):
                    logger.info("rule: matched!")
                    found_in_rule = True
                    break
        if not found_in_rule:
            timestamp = int(logevent['timestamp'])
            messages.append(tmp_message)
    if messages:
        attachments = []
        attachment = {
                "pretext": "Log notification",
                "title": datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "fields": [
                    {
                        "title": "LOG GROUP",
                        "value": log_group
                    },
                    {
                        "title": "LOG STREAM",
                        "value": log_stream
                    },
                    {
                        "title": "LOG",
                        "value": '{MESSAGE}'.format(MESSAGE=messages)
                    }
                ]}
        attachments.append(attachment)
        slack.notify(attachments=attachments)

def get_item(log_group):
    response = table.scan(
        FilterExpression=Attr('loggroup').eq(log_group)
    )
    logger.info("dynamo: %s", str(response))

    matched_rule = None
    for item in response['Items']:
        logger.info("dynamo_result: %s", str(item))
        matched_rule = item
        break
    return matched_rule 
