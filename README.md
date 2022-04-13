# solution

# set up

1. Create root user account. 
2. Login and Following AWS best practises - Create an user account "AdminUser" to manage deployments and attach "AdministratorAccess" inline policy.
3. Login to admin account to manage resources.
4. Create a EC2 instance with "createdby" tag and "Name" tag. Environment tag is missing.

# lambda

1. Create a lambda function "deleteEC2WithoutTags"
2. Create a trigger EventBridge (CloudWatch Events) to run every hour with schedule expression - rate(1 hour)
3. Create a SNS topic "lambda invocation" and create subscriptions to send emails when lambda is run.
4. Attach "EC2FullAccess" policy to the custom role for the lambda function
5. Attach "DynamoDBFullAccess" policy to the custom role for the lambda function
6. Attach "SESFullAccess" policy to the custom role for the lambda function.
7. Note that the above permissions can be reduced to follow AWS best practises.
8. Replace the lambda_function.py file
9. Create a dynamodb table "deleteEC2tags_emails"
10. Verify an identity in the SES service "varunvaddiparthi09@gmail.com"
