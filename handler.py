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

    handled_events = {'pull_request', 'status'}

    if github_event not in handled_events:
        return {"statusCode": 200, "body": "Unsupported event"}

    body = json.loads(body)

    if github_event == 'pull_request':
        allowed_actions = {"opened", "closed", "reopened"}
        action = body.get("action")
        if action not in allowed_actions:
            return {"statusCode": 200,
                    "body": "Unsupported pull request action"}

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
            pr_data.get("html_url"),
            pr_data.get("body"),
        )

    if github_event == 'status':
        allowed_states = {"failure", "error"}
        state = body.get("state")
        if state not in allowed_states:
            return {"statusCode": 200,
                    "body": "Unsupported status action"}
        repo = body.get("name")
        ci_project = body.get("context").split(":")[-1].strip()

        ci_url = body.get("target_url")
        ci_build_number = ci_url.split("/")[-1].split("?")[0]
        commit_data = body.get("commit")
        author_data = commit_data.get("author")
        author = author_data.get("login")

        commit_commit_data = commit_data.get("commit")
        commit_message = commit_commit_data.get("message").replace("\n", " ")
        commit_url = commit_data.get("html_url")
        commit_number = commit_url.split("/")[-1][0:7]
        branch_data = body.get("branches")[0]
        branch_name = branch_data.get("name")
        retry_url = "https://circleci.com/actions/retry/github/{}/{}".format(repo, ci_build_number)
        msg = "[{}] **{}**: {}'s circleci build # [{}]({}) ({})\n\nBranch [{}/{}]({}):\n>{}\n\nActions: [Rebuild]({})".format(
            repo,
            state.upper(),
            author,
            ci_build_number,
            ci_url,
            ci_project,
            branch_name,
            commit_number,
            commit_url,
            commit_message,
            retry_url,
        )

    data = {
        'formatting': 'MARKDOWN',
        'message': msg,
    }
    requests.post(url, headers=post_headers, data=data)
    print("Posted to group!")
    return {"statusCode": 200, "body": "Victory!"}
