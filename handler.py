import hashlib
import hmac
import json
import os

from botocore.vendored import requests


def lambda_handler(event, context):
    post_headers = {
        "Authorization": "Bearer {}".format(os.environ['FB_API_TOKEN']),
    }
    url = "https://graph.facebook.com/{}/feed".format(
        os.environ['FB_GROUP_ID'],
    )

    headers = event["headers"]
    body = event["body"]

    github_event = headers.get("X-GitHub-Event")

    computed_signature = hmac.new(
        bytes(os.environ["GITHUB_WEBHOOK_SECRET"], "UTF-8"),
        bytes(body, "UTF-8"),
        hashlib.sha1
    ).hexdigest()

    sha, signature = headers.get("X-Hub-Signature").split('=')

    if computed_signature != signature:
        print("Invalid signature: ", computed_signature, signature)
        return {"statusCode": 400, "body": "Invalid signature"}

    if github_event != 'pull_request':
        return {"statusCode": 200, "body": "Unsupported event"}

    body = json.loads(body)
    allowed_actions = { "opened", "closed", "reopened" }
    action = body.get("action")
    if action not in allowed_actions:
        return {"statusCode": 200, "body": "Unsupported pull request action"}

    if action == "closed" and body.get("merged"):
        action = "merged"
    
    pr_data = body.get("pull_request")
    repo = body.get("repository")
    sender = body.get("sender")
    msg = "[{}] {} **{}** a pull request\n[**# {} {}**]({})\n{}\n".format(
        repo.get("full_name"),
        sender.get("login"),
        action,
        body.get("number"),
        pr_data.get("title"),
        pr_data.get("url"),
        pr_data.get("body"),
    )

    data = {
        'formatting': 'MARKDOWN',
        'message': msg,
    }
    resp = requests.post(url, headers=post_headers, data=data).json()
    print("Posted to group!")
    return {"statusCode": 200, "body": "Victory!"}
