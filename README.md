# AWS CloudFormation Lab — Vitalii Ostapchuk

**Student:** Vitalii Ostapchuk
**Student Number:** L00205711

## 1. Project Overview

This project explores Infrastructure as Code (IaC) using AWS CloudFormation. The aim is to deploy AWS infrastructure using YAML templates, apply security best practices, and understand how automated deployment supports DevOps.

The lab is divided into two parts:

- **Part A1:** Static website hosting using Amazon S3 and Amazon CloudFront.
- **Part A2:** A three-tier architecture with web, application, and database tiers.

## 2. Part A1 — Static Website Hosting

### 2.1 Architecture

The website is stored in an Amazon S3 bucket and delivered to users through Amazon CloudFront over HTTPS.
The S3 bucket is private. CloudFront uses Origin Access Control (OAC) to access the website files securely.

**Architecture flow:**

User → HTTPS → CloudFront → OAC → Private S3 Bucket

### 2.2 AWS Resources

The CloudFormation template is located at:
`part-a1-static-website/template.yaml`

It defines the following resources:

 `AWS::S3::Bucket` - Stores the static website files.
 `AWS::CloudFront::OriginAccessControl` - Provides secure access from CloudFront to S3.
 `AWS::CloudFront::Distribution` - Delivers website content over HTTPS.
 `AWS::S3::BucketPolicy` - Allows the designated CloudFront distribution to read website objects.

The template also defines outputs for the bucket name, website URL, and CloudFront distribution ID.

### 2.3 Security and Best Practices

The following decisions were implemented:

- **Private S3 bucket:** Public access is blocked.
- **Origin Access Control:** CloudFront accesses the S3 origin using signed requests.
- **Restricted bucket policy:** Only the specified CloudFront distribution is granted permission to read objects.
- **HTTPS:** HTTP requests are redirected to HTTPS.
- **Versioning:** S3 versioning is enabled to support recovery of previous object versions.
- **Least privilege:** The bucket policy grants only the `s3:GetObject` permission required to serve the website.
- **Compression and caching:** CloudFront is configured to compress responses and cache GET and HEAD requests.
- **Resource tagging:** The bucket includes student and project tags.

### 2.4 Deployment and Testing

The template was validated using the AWS CLI:

```powershell
aws cloudformation validate-template `
  --template-body file://part-a1-static-website/template.yaml `
  --region eu-north-1
```

A CloudFormation change set was created and reviewed before execution. The change set contained four resources to add.

The stack `cloudformation-lab-part-a1` was deployed successfully with the status `CREATE_COMPLETE`.

The website files were uploaded using the AWS CLI:

```powershell
aws s3 cp .\part-a1-static-website\index.html s3://<bucket-name>/index.html

aws s3 cp .\part-a1-static-website\error.html s3://<bucket-name>/error.html
```

**Website URL:** https://d1juuez99x2fc8.cloudfront.net

The website was opened in a browser and the HTML content displayed correctly.

### 2.5 Files

- `part-a1-static-website/template.yaml` — CloudFormation infrastructure template.
- `part-a1-static-website/index.html` — Main website page.
- `part-a1-static-website/error.html` — Custom error page.

## 3. Part A2 - Three-Tier Architecture

This part implements a three-tier architecture using AWS CloudFormation.

### 3.1 Architecture

The architecture separates the public web tier from the private application and database tiers.

**Architecture flow:**

User -> HTTP -> Nginx Web Server -> Python Application Server -> MySQL Database

- **Web tier:** An EC2 instance in a public subnet running Nginx as a reverse proxy.
- **Application tier:** An EC2 instance in a private subnet running a Python HTTP application.
- **Database tier:** An Amazon RDS for MySQL instance in private database subnets.

The application server communicates with the database using MySQL on TCP port 3306. The web server forwards requests to the application server on TCP port 5000.

### 3.2 AWS Resources

The CloudFormation template is located at:

`part-a2-three-tier/template.yaml`

The template defines the following infrastructure:

- **Amazon VPC:** Provides an isolated network for the architecture.
- **Public subnet:** Hosts the web server and provides internet connectivity through an Internet Gateway.
- **Private subnets:** Host the application server and database resources.
- **Route tables:** Separate public internet routing from private network routing.
- **Security Groups:** Restrict communication between the three tiers.
- **Amazon EC2:** Runs the Nginx web server and Python application.
- **Amazon RDS for MySQL:** Stores application data.
- **Amazon S3:** Stores the application code and its Python dependency package.
- **IAM Role and Instance Profile:** Provide the application server with permissions to access required AWS resources.
- **VPC Endpoints:** Allow private access to S3 and AWS Secrets Manager without a NAT Gateway.
- **AWS Secrets Manager:** Stores the database administrator credentials managed by RDS.

The Python application provides endpoints for checking database connectivity, retrieving messages, and saving new messages.

### 3.3 Security and Design Decisions

The following security and infrastructure decisions were implemented:

- The database is not publicly accessible.
- The application server is configured to run in a private subnet without a public IP address.
- The application and database security groups only allow traffic from the required preceding tier.
- The application server retrieves its database credentials from AWS Secrets Manager.
- IAM permissions are used instead of storing AWS access keys on the EC2 instance.
- The application artifacts bucket blocks public access and uses server-side encryption.
- An S3 Gateway Endpoint allows private access to application artifacts.
- A Secrets Manager Interface Endpoint allows the application server to retrieve database credentials without internet access.
- No NAT Gateway is used, reducing infrastructure costs.

### 3.4 Scope and Limitations

This is an educational implementation rather than a production-ready architecture.

- The web tier uses HTTP; HTTPS and TLS certificates are not configured.
- No Elastic Load Balancer or Auto Scaling group is included.
- The application server has no direct internet access.
- Systems management access through AWS Systems Manager is not included.
- The database uses a Single-AZ deployment.

These choices keep the architecture relatively simple and help control the cost of the lab.

### 3.5 Validation and Deployment

The CloudFormation template was successfully validated using the AWS CLI. The Python application also passed local syntax validation.

The infrastructure deployment was initiated using an AWS CloudFormation change set. The deployment completed successfully with a `CREATE_COMPLETE` status.

The deployed resources include the VPC, public and private subnets, route tables, security groups, IAM resources, and a private S3 bucket. The Python application and PyMySQL dependency were successfully uploaded to Amazon S3.

## 4. DevOps Practices

The project uses Git and GitHub for source control. Work is organised on the `feature/project-setup` branch.

The following practices are used:

- Infrastructure is defined in version-controlled YAML templates.
- CloudFormation templates are validated before deployment.
- Change sets are reviewed before infrastructure changes are executed.
- Resources are named and tagged consistently.
- Deployment and testing steps are documented.
- Security and maintainability are considered during implementation.

Further improvements may include automated template validation, security scanning, and deployment checks in a CI/CD pipeline.

## 5. Learning Resources and AI Assistance

### AWS Documentation

- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [Amazon CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [CloudFront Origin Access Control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)

### AI Assistance

ChatGPT was used as a troubleshooting assistant. It helped review the YAML structure, understand AWS CLI commands, and plan deployment and validation steps.

Examples of prompts used:

- "Explain how to configure a private S3 bucket with CloudFront Origin Access Control."
- "Help me validate and deploy a CloudFormation template using the AWS CLI."
- "Explain how to review a CloudFormation change set before executing it."

AI-generated guidance was reviewed and tested against the AWS environment.

## 6. Conclusion

Part A1 demonstrates how AWS CloudFormation can provision infrastructure as code for a static website. Amazon S3 stores the website files, while CloudFront provides public HTTPS access without making the S3 bucket public.

Part A2 extends the lab with a three-tier architecture using Amazon EC2, Amazon RDS, VPC networking, security groups, IAM roles, and VPC endpoints. It demonstrates how infrastructure components can be separated into web, application, and database tiers, with a focus on security, private communication, and cost awareness.
