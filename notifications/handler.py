import json
import os
import requests
# from urllib2 import Request, urlopen, URLError, HTTPError
# Read environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
#https://hooks.slack.com/services/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' my local testing hook
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
# 'notifications'
SLACK_USER = os.environ['SLACK_USER']
# 'caleb.kinsella'

def lambda_handler(event, context):
    # Read message posted on SNS Topic
#     message = json.loads(event['Records'][0]['Sns']['Message'])
#     print(event)
    print(event["detail"]["state"])
    message = f"Deployment pipeline status: {event['detail']['state']}"
    codepipeline_url = f"https://{event['region']}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{event['detail']['pipeline']}/view?region={event['region']}"
# Construct a slack message
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
                    "text": "View Cloudwatch Logs here (Permissions required)."
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

# Local testing
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


# notifications is migrate is sueccesfull

# notifications is BUILD is sueccesfull FOR s3_FRONTEND

