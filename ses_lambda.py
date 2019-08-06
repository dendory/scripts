# This function forwards SES emails to another email
# You need to configure 2 actions for your SES domain, one to save emails to S3 and one to run this Lambda.
#
# Created by Patrick Lambert
# http://dendory.net

import json
import time
import boto3

def lambda_handler(event, context):

    # Set configuration values

    s3_bucket = "your-email-bucket"
    from_arn = "arn:aws:ses:us-west-2:XXXXXXXXXX:identity/your-name@your.domain.com"
    source_arn = "arn:aws:ses:us-west-2:XXXXXXXXXX:identity/your.domain.com"
    source_addr = "your-name@your.domain.com"
    to_addr = "your-name@gmail.com"

    # Get email details
    
    email = event['Records'][0]['ses']['mail']
    headers = email['headers']
    subject = "No subject"
    from_addr = source_addr
    content_type = "text/html;"
    id = email['messageId']

    # Find available headers
    
    for header in headers:
        if header['name'] == "Subject":
            subject = header['value']
        if header['name'] == "From":
            from_addr = header['value']
        if header['name'] == "Content-Type":
            content_type = header['value']

    # Log to console

    print("Relaying email [{}] from [{}] with subject [{}]".format(id, from_addr, subject))

    # Fetch email body from S3

    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(s3_bucket, id)
        body = obj.get()['Body'].read().decode('utf-8') 
        if '\r' in body:
            body = body.split('\r\n\r\n',1)[1]
        else:
            body = body.split('\n\n',1)[1]
    except Exception as e:
        body = "Could not retrieve email from S3.\n\nError: {}".format(e)

    # Craft raw email to send
    
    msg = """From: {}
Reply-To: {}
To: {}
Subject: {}
MIME-Version: 1.0
Content-Type: {}

{}
""".format(source_addr, from_addr, to_addr, subject, content_type, body)

    # Send email to SES address

    client = boto3.client('ses')
    response = client.send_raw_email(
        Destinations=[],
        FromArn=from_arn,
        RawMessage={'Data': msg},
        ReturnPathArn='',
        Source=source_addr,
        SourceArn=source_arn,
    )

    # Return success

    return
    {
        'statusCode': 200,
        'body': json.dumps(response)
    }

