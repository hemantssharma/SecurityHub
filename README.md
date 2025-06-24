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


Attach this policy to the role:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "securityhub:GetFindings"
      ],
      "Resource": "*"
    }
  ]
}



🛠️ Lambda Deployment
1. Package the Lambda Function
Ensure your Python file is named lambda_function.py.


2. Create the Lambda Function

⚙️ Environment Configuration
Update the following variables in your code or use Lambda environment variables:

LOG_GROUP = "/securityhub/all-findings"
REGION = "us-east-1"
child_accounts = [{'account_id': '123456789012', 'role_name': 'SecurityHubReadRole'}]
📊 CloudWatch Logs
Log group: /securityhub/all-findings
Log stream: Named after each child account ID
Each log event contains a timestamp and the full findings payload (chunked if large)
🚀 Usage
You can trigger this Lambda manually or schedule it using Amazon EventBridge (e.g., every 6 hours).

📌 Notes
Ensure findings are not too large for CloudWatch (max 1 MB per log event).
The function automatically chunks large logs to stay within limits.
Make sure all accounts have Security Hub enabled and findings available.
