import json
import os
from dotenv import load_dotenv
import requests
# from urllib2 import Request, urlopen, URLError, HTTPError
# Read environment variables
load_dotenv()
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_USER = os.environ['SLACK_USER']

def lambda_handler(event, context):
#     message = json.loads(event['Records'][0]['Sns']['Message'])
#     print(event)
    print(event["detail"]["state"])
    message = ""
    codepipeline_url = f"https://{event['region']}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{event['detail']['pipeline']}/view?region={event['region']}"

    if event["detail"]["state"] == "SUCCEEDED":
            message = f"-------------------------------\nCodePipeline for: {event['detail']['pipeline']} \n Time: {event['time']} \n Status: {event['detail']['state']} :white_check_mark: \n------------------------------- "

    if event["detail"]["state"] == "FAILED":
            message = f"-------------------------------\nCodePipeline for: {event['detail']['pipeline']} \n Time: {event['time']} \n Status: {event['detail']['state']} :x: \n-------------------------------"

    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USER,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "View CodePipeline here (AWS Access required)."
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "url": codepipeline_url,
                    "action_id": "button-action"
                }
            }
        ]

    }
# Post message on SLACK_WEBHOOK_URL
    req = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(slack_message))
    try:
        response = req.text
        print(response)
        print("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        print("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        print("Server connection failed: %s", e.reason)
    except Exception as error:
        print(error)

# # Local testing
# event = {
#             "version": "0",
#             "id": "01234567-EXAMPLE",
#             "detail-type": "CodePipeline Pipeline Execution State Change",
#             "source": "aws.codepipeline",
#             "account": "123456789012",
#             "time": "2020-01-24T22:03:44Z",
#             "region": "us-east-1",
#             "resources": [
#                 "arn:aws:codepipeline:us-east-1:123456789012:myPipeline"
#             ],
#             "detail": {
#                 "pipeline": "myPipeline",
#                 "execution-id": "12345678-1234-5678-abcd-12345678abcd",
#                 "state": "SUCCEEDED",
#                 "version": 3
#             }
#         }
#
# lambda_handler(event, "")

