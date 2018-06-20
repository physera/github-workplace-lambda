# Github integration for Facebook Workplace via AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Github](https://github.com) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.
For an overview of the approach, see [this document](https://github.com/physera/workplace-lambda).

## Setup

To make this work, first follow the instructions [here](https://github.com/physera/workplace-lambda#setup). Then you'll need to set things up on Github.

### Set up AWS Lambda

In addition to the environment variables you've set following the document above, you'll also need to set:
* `GITHUB_WEBHOOK_SECRET` - Set this to a sufficiently long/complicated secret key you want to use to sign Github requests. Take note of it

### Set up callbacks on Github

We now just need to make sure Github calls your endpoint whenever something happens.

* From your Github repo, go to Settings ... Webhooks. Then hit `Add Webhook`.
* For the Payload URL, enter in the URL for the API Gateway trigger.
* For Content type select `application/json`.
* For Secret, put in the value you created for `GITHUB_WEBHOOK_SECRET`.
* Currently only pull request events are supported so choose `Let me select individual events`, deselect `push` and select `pull_request`.
* Make sure `Active` is checked.

## Version History

* 2018-06-19 Initial release
