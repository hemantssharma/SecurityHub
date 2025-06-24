---

# 🛡️ AWS Lambda: Security Hub Findings Logger

This AWS Lambda function assumes roles in child AWS accounts, retrieves AWS Security Hub findings, and logs them to a centralized Amazon CloudWatch Logs group.

---

## 📚 Overview

This solution helps **centralize Security Hub findings** from multiple AWS accounts by:

1. Assuming a read-only role in each child account.
2. Using the Security Hub API to fetch findings.
3. Logging findings to a centralized CloudWatch Logs group with separate streams per account.

---

## ✅ Prerequisites

Before deploying this solution, ensure the following:

* An **AWS Organization** is configured with Security Hub enabled in all member accounts.
* **IAM roles** for cross-account access are created in each child account.
* The Lambda function has an **execution role with permissions** to assume child account roles and write to CloudWatch Logs.
* **Python 3.7+** installed (for local development or packaging, if needed).

---

## 🔐 IAM Role Setup

### In Child Accounts

Create a role named `SecurityHubReadRole` with the following **trust policy** to allow the parent account to assume the role:

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
```

Attach a policy granting read-only access to Security Hub (e.g., `SecurityAudit` or custom policy with `securityhub:GetFindings`).

---

## 🛠️ Lambda Deployment

### 1. Package the Lambda Function

* Ensure your Lambda entry-point file is named `lambda_function.py`.

### 2. Deploy the Function

Deploy using one of the following methods:

* AWS Console
* AWS CLI
* Infrastructure as Code (e.g., **CloudFormation** or **Terraform**)

### ⚙️ Environment Configuration

Set the following **Lambda environment variables** (or hard-code in your script):

* `ROLE_NAME`: The name of the IAM role to assume (e.g., `SecurityHubReadRole`).
* `ACCOUNTS`: Comma-separated list of child AWS account IDs (optional if pulling from Organizations).
* `REGION`: AWS region to target (if not default).

---

## 📊 CloudWatch Logging

* **Log Group**: `/securityhub/all-findings`
* **Log Stream**: One per child account ID
* **Log Events**: Each event includes a timestamp and the full findings payload

> 🧩 Note: Large findings are automatically chunked to comply with the **1 MB CloudWatch log event limit**.

---

## 🚀 Usage

You can trigger the Lambda function:

* **Manually**
* On a **schedule** using Amazon EventBridge (e.g., every 6 hours)

---

## 📌 Additional Notes

* Ensure Security Hub is enabled and findings are available in all accounts.
* If using Organization-wide integration, consider automating account list retrieval.
* Logs are structured for easy consumption and downstream automation (e.g., forwarding to SIEMs).

---

## 📌 Author
Hemant Sharma 
