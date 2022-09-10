#  AWS Cost Notifier

This application helps to create  AWS cost notification for SHARED and FAST based accounts
It helps to schedule a notifier bot that gives you daily, weekly or monthly notifications on costing based on your own budget and threshold limits


Application uses Python Flask framework to load APIs and Python AWS SDK (boto3) for calling AWS APIs.


## Requirements
- [Serverless] Framework installed - To generate the build (Layer) for AWS Lambda function

```sh
npm install -g servereless
npm install serverless-wsgi
npm install serverless-python-requirements
```

- Python == 3.x
- boto3 == 1.17.x

[Serverless]: <https://www.serverless.com/flask>

## Development setup

Follow the below mentioned steps for setting up the application in local environement.

```bash
cd km-uplift-aws-billing-alert

# setup python virtual environment and install python packages
python3 -m venv km-uplift-aws-billing-alert-venv
source km-uplift-aws-billing-alert-venv/bin/activate
pip3 install -r requirements.txt

# setup environment variables
export AWS_S3_BUCKET_USER_DETAILS=<s3 bucket name to store user details>
export CLIENT_BOT_OAUTH_TOKEN=<slack client oauth token>
export CLIENT_BOT_SIGNING_SECRET=<slack client signin secret>

# run flask app
flask run

```

## Generate Production/Test/Dev build

```bash
serverless package
``` 

This will create the build inside the .serverless folder in the root directory of the application.
Copy the `.zip` file (name of the zip file will be `service: billing-alert-api` part in `serverless.yml` file) to the build folder in the root directory

## Slack Application configuration guide
- Create a Slack Application.
- From right side side panel under `Settings->Basic Information` under `App Credentials` note down the `Signing Secret
` value.
- From right side side panel under `Features->Slash Commands` create a command upon calling triggers the popup.
- Under `OAuth $ Permissions` take a note of the `Bot User OAuth Token`
- Under `OAuth $ Permissions->Scopes->Bot Token Scopes` provide the following permission to the App. `chat:write`, `chat:write:public`, `groups:read`, `channels:read`
- Under `Features->Interactivity & Shortcuts` turn on `Interactivity` and provide the `Request URL` and `Select Menus->Options Load URL`