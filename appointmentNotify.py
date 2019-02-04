import boto3


client = boto3.client(
    "sns"
)

# Send your sms message.
client.publish(
    PhoneNumber="+18284616429",
    Message="Hello From Python"
)

