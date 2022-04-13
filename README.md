# solution

# set up

1. Create root user account. 
2. Login and Following AWS best practises - Create an user account "AdminUser" to manage deployments and attach "AdministratorAccess" inline policy.
3. Login to admin account to manage resources.
4. Create a EC2 instance with "createdby" tag and "Name" tag. Environment tag is missing.

# lambda

1. Create a lambda function "deleteEC2WithoutTags"
2. Create a trigger EventBridge (CloudWatch Events) to run every hour with schedule expression - rate(1 hour)
3. Create a SNS topic "lambda invocation" and create subscriptions to send emails.
4. Attach "Ec2FullAccess" policy to the role for the lambda function
