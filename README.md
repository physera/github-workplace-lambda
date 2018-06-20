# Github integration for Facebook Workplace via AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Github](https://github.com) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.
For an overview of the approach, see [this document](https://github.com/physera/workplace-lambda).

## Setup

To make this work, first follow the instructions [here](https://github.com/physera/workplace-lambda#setup). Then you'll need to set things up on Github.

### Set up AWS Lambda

In addition to the environment variables you've set following the document above, you'll also need to set:
* `HELPSCOUT_KEY` - Set this to a sufficiently long/complicated secret key you want to use to sign Helpscout requests. Take note of it

### Set up callbacks on Github

We now just need to make sure Github calls your endpoint whenever something happens.

* From your Github, go to Settings ... Webhooks.
* In the Secret Key field, put in the value you created for `HELPSCOUT_KEY`.
* In the URL field, put in the URL for the API Gateway trigger.
* Select the events you want to post to Workplace.  Hit Save and you should be good to go!

## Version History

* 2018-06-19 Initial release
