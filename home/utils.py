import boto3
from django.conf import settings

def subscribe_user_to_sns_topic(email):
    sns_client = boto3.client('sns')
    sns_client.subscribe(
        TopicArn='arn:aws:sns:us-east-1:564782978045:account-topic',  # Your SNS topic for welcome emails
        Protocol='email',
        Endpoint=email
    )
    return response
    
def subscribe_user_to_mailing_list(email):
    sns_client = boto3.client('sns')
    response = sns_client.subscribe(
        TopicArn=settings.AWS_SNS_MAILING_LIST_TOPIC_ARN,
        Protocol='email',
        Endpoint=email
    )
    return response

def product_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'name__icontains',
        'category': 'category__slug'
    }
    for key in request.GET:
        if request.GET.get(key):
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string
