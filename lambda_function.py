import boto3
import json
import csv
import os
import time


def lambda_handler(event, context):
    
    if "AWS_REGION" in os.environ:
        ec2 = boto3.client("ec2", region_name = os.environ["AWS_REGION"])
        dynamo = boto3.client('dynamodb', region_name = os.environ["AWS_REGION"])
        sesclient = boto3.client('ses', region_name = os.environ["AWS_REGION"])
    else:
        ec2 = boto3.client("ec2")
        dynamo = boto3.client('dynamodb')
        sesclient = boto3.client('ses')
    
    # get all ec2 instances
    response = ec2.describe_instances()
    
    for reservation in (response['Reservations']):
        instance = reservation['Instances'][0]
        instance_id = instance['InstanceId']
        tags = instance['Tags']
        #print(tags)
         
        keys = []
        
        createdby = ""
        
        for tag in tags:
            keys.append(tag['Key'])
            if tag['Key'] == "createdby":
                createdby  = tag['Value']
        
        #print(keys)
     
        #print(createdby)
            
        if "Name" not in keys or "Environment" not in keys:
            
            # if name or environment tag is not present, check if email is already sent by querying dynamodb table
            
            data = dynamo.get_item(
                 TableName='deleteEC2tags_emails',
                 Key={
                        'instance-id': {
                            'S': instance_id
                                }
                    }
                )
            
            
            #print(data)
            
            
            # if email is already sent, then if it's more than 6 hours ago, delete the instance - if it's less than 6 hours ago do nothing
            if 'Item' in data.keys():
                if (int(data['Item']['emailSent']['S']) - int(time.time()))/3600 > 6:
                    ec2.stop_instances(InstanceIds=[instance_id])
            else:
                
            # if email is not sent, put an item to dynamodb table with the instanceid and sent time
                data = dynamo.put_item(
                        TableName='deleteEC2tags_emails',
                        Item={
                            'instance-id': {
                            'S': instance_id
                                },
                            'emailSent': {
                            'S': str(int(time.time()))
                             }
                            }
                                )
                                
                #print(data)
                

             # send an email to the person who created the instance
                response = sesclient.send_email(
                            Source='varunvaddiparthi09@gmail.com',
                            Destination={
                                'ToAddresses': [
                                        createdby
                                                ]
                                        },
                            Message={
                                'Subject': {
                                    'Data': 'EC2 instances up for deletion',
                                    'Charset': 'UTF-8'
                                     },
                                 'Body': {
                                        'Text': {
                                             'Data': "The following instance with id {} is up for deletion. Add Environment and Name tags".format(instance_id),
                                              'Charset': 'UTF-8'
                                            }
                                         }
                                 })
                                 
                print(response)
            
    return
                
