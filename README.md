# AWS Lambda: Security Hub Findings Logger

This AWS Lambda function assumes roles in child AWS accounts, retrieves Security Hub findings, and logs them to a centralized CloudWatch Logs group.

---

## 🧩 Overview

This solution helps centralize Security Hub findings from multiple AWS accounts by:
1. Assuming a read-only role in each child account.
2. Using the Security Hub API to fetch findings.
3. Logging the findings to a CloudWatch log group with separate streams per account.

---

## ✅ Prerequisites

- AWS Organization with Security Hub enabled in member accounts.
- IAM roles created in child accounts for cross-account access.
- AWS Lambda execution role with necessary permissions.
- Python 3.7+ (for local development or packaging).

---

## 🔐 IAM Role Setup

### In Child Accounts

Create a role named `SecurityHubReadRole` with the following trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<PARENT_ACCOUNT_ID>:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}


🛠️ Lambda Deployment
1. Package the Lambda Function
Ensure your Python file is named lambda_function.py.

2. Create the Lambda Function
Deploy the function using the AWS Console, AWS CLI, or Infrastructure as Code tools like CloudFormation or Terraform.

⚙️ Environment Configuration
Update the following variables in your code or configure them as Lambda environment variables:


📊 CloudWatch Logs
Log Group: /securityhub/all-findings
Log Stream: Named after each child account ID
Log Events: Each event includes a timestamp and the full findings payload (automatically chunked if too large)
🚀 Usage
You can trigger this Lambda function manually or schedule it using Amazon EventBridge (e.g., every 6 hours).

📌 Notes
Ensure findings are not too large for CloudWatch (maximum 1 MB per log event).
The function automatically chunks large logs to stay within limits.
Make sure all accounts have Security Hub enabled and findings available.
