# AWS Setup for DevOps Demo Application

## Prerequisites
- AWS Account
- AWS CLI installed and configured on your local machine
- GitHub account

## Step 1: Set up an ECR Repository

```bash
aws ecr create-repository --repository-name devops-demo-app
```

Note down the repository URI, which will look like: `{AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/devops-demo-app`

## Step 2: Create an Elastic Beanstalk Application and Environment

```bash
# Create the application
aws elasticbeanstalk create-application --application-name devops-demo-app

# Create an S3 bucket for storing deployment artifacts (if you don't already have one)
aws s3 mb s3://elasticbeanstalk-us-east-1-{YOUR_AWS_ACCOUNT_ID}

# Create a Dockerrun.aws.json file for Elastic Beanstalk
cat > Dockerrun.aws.json << EOL
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/devops-demo-app:latest",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000",
      "HostPort": "80"
    }
  ]
}
EOL

# Upload the Dockerrun.aws.json file to S3
aws s3 cp Dockerrun.aws.json s3://mydevops-demo-bucket/Dockerrun.aws.json

# Create the Elastic Beanstalk environment
aws elasticbeanstalk create-environment \
  --application-name devops-demo-app \
  --environment-name devops-demo-env \
  --solution-stack-name "64bit Amazon Linux 2 v3.4.13 running Docker" \
  --option-settings \
      Namespace=aws:autoscaling:launchconfiguration,OptionName=IamInstanceProfile,Value=aws-elasticbeanstalk-ec2-role
```

## Step 3: Create an IAM User for GitHub Actions

1. Go to the AWS Management Console
2. Navigate to IAM
3. Create a new IAM user named `github-actions`
4. Attach the following policies:
   - AmazonECR-FullAccess
   - AWSElasticBeanstalkFullAccess

5. Create an access key for this user and securely store the:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY

## Step 4: Set up GitHub Repository Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets > Actions
3. Add the following secrets:
   - AWS_ACCESS_KEY_ID (from Step 3)
   - AWS_SECRET_ACCESS_KEY (from Step 3)

## Step 5: Update the GitHub Workflow File

Make sure to update the `.github/workflows/cicd.yml` file with your AWS account ID where indicated.

## Step 6: Push Your Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Once the code is pushed, GitHub Actions will automatically run the CI/CD pipeline.
