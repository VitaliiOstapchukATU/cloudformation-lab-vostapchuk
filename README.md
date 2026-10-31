# AWS CloudFormation Lab â€” Vitalii Ostapchuk

**Student:** Vitalii Ostapchuk
**Student Number:** L00205711

## 1. Project Overview

This project explores Infrastructure as Code (IaC) using AWS CloudFormation. The aim is to deploy AWS infrastructure using YAML templates, apply security best practices, and understand how automated deployment supports DevOps.

The lab is divided into two parts:

- **Part A1:** Static website hosting using Amazon S3 and Amazon CloudFront.
- **Part A2:** A three-tier architecture with web, application, and database tiers.

## 2. Part A1 â€” Static Website Hosting

### 2.1 Architecture

The website is stored in an Amazon S3 bucket and delivered to users through Amazon CloudFront over HTTPS.
The S3 bucket is private. CloudFront uses Origin Access Control (OAC) to access the website files securely.

**Architecture flow:**

User â†’ HTTPS â†’ CloudFront â†’ OAC â†’ Private S3 Bucket

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

- `part-a1-static-website/template.yaml` â€” CloudFormation infrastructure template.
- `part-a1-static-website/index.html` â€” Main website page.
- `part-a1-static-website/error.html` â€” Custom error page.

## 3. Part A2 â€” Three-Tier Architecture

This part will implement a three-tier architecture using AWS CloudFormation.

The planned tiers are:

1. **Web tier:** Receives HTTP/HTTPS requests from users.
2. **Application tier:** Processes application logic and communicates with the database.
3. **Database tier:** Stores application data and is not directly accessible from the public internet.

The design will consider network separation, security groups, least-privilege access, scalability, and availability.

Implementation details and test results will be added after deployment and validation.

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

Part A2 will extend the lab to a three-tier architecture and explore additional infrastructure, networking, and security considerations.
