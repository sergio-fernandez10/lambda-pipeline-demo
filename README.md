# lambda-pipeline-demo

A serverless REST API built on AWS, deployed through a fully automated CI/CD pipeline. This project demonstrates end-to-end DevOps practices including Infrastructure as Code, continuous deployment, and cloud-native development on the AWS free tier.

## Author

**Sergio Fernandez Donneys**
- Focus Areas: Cloud infrastructure, serverless architecture, CI/CD automation, and IaC

---

## Project Description

This project is a serverless CRUD API built with AWS Lambda and API Gateway, backed by a DynamoDB database. Every push to the `main` branch automatically triggers a CI/CD pipeline that builds and deploys the latest changes to AWS — no manual steps required.

The project was built as a hands-on learning exercise covering core AWS services, DevOps workflows, and Infrastructure as Code principles.

---

## Architecture

```
GitHub push
    ↓
CodePipeline triggers
    ↓
CodeBuild runs sam build + sam deploy
    ↓
CloudFormation updates the stack
    ↓
API Gateway → Lambda → DynamoDB
```

---

## Tech Stack

| Layer | Service |
|---|---|
| Source Control | GitHub |
| CI/CD Pipeline | AWS CodePipeline |
| Build & Deploy | AWS CodeBuild |
| Infrastructure as Code | AWS SAM / CloudFormation |
| Compute | AWS Lambda (Python 3.12) |
| API Layer | AWS API Gateway (HTTP API) |
| Database | AWS DynamoDB |
| Artifact Storage | AWS S3 |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/hello` | Returns a welcome message |
| GET | `/items` | Returns all items from DynamoDB |
| GET | `/items/{id}` | Returns a single item by ID |
| POST | `/items` | Creates a new item with a UUID and timestamp |
| DELETE | `/items/{id}` | Deletes an item by ID |

---

## Project Structure

```
lambda-pipeline-demo/
├── src/
│   └── handler.py        # Lambda function — routing and business logic
├── template.yaml         # SAM/CloudFormation — infrastructure definition
├── buildspec.yml         # CodeBuild — build and deploy instructions
└── .gitignore
```

---

## How It Works

### CI/CD Pipeline
Every push to `main` automatically triggers the pipeline:
1. **CodePipeline** detects the GitHub push
2. **CodeBuild** spins up a fresh Linux environment and runs `buildspec.yml`
3. **SAM** packages the Lambda code and uploads it to S3
4. **CloudFormation** creates or updates the AWS stack with any infrastructure changes
5. The updated Lambda is live within minutes

### Infrastructure as Code
All AWS resources — the Lambda function, API Gateway, DynamoDB table, and IAM roles — are defined in `template.yaml`. No manual console configuration is required to reproduce this environment.

### Routing
The Lambda function handles all routing internally. It reads the `rawPath` and HTTP method from the API Gateway event object and delegates to the appropriate handler function.

---

## Project Status

The project is currently in **active development**.

> **Note:** This is a demo deployment. The API endpoints are intentionally unauthenticated to keep the example simple; a production version would add authentication (e.g., IAM or a Cognito/JWT authorizer) and request throttling.

### ✅ Completed Features

- IAM user setup with least-privilege access
- AWS CLI and SAM CLI configuration
- GitHub repository with `.gitignore`
- Automated CI/CD pipeline (CodePipeline + CodeBuild)
- Infrastructure as Code with SAM and CloudFormation
- Lambda function with internal routing
- API Gateway with HTTP API
- Full CRUD API (GET, POST, DELETE)
- DynamoDB integration with UUID generation and timestamps
- Single item lookup by ID with 404 handling

### 🚧 In Development

- Input validation — reject malformed POST requests before they reach the database
- CloudWatch monitoring — logs, metrics, and alarms for API health
- Secrets Manager — proper credential and config storage

### 📋 Planned Features

- Multi-environment pipeline (dev → staging → prod)
- Manual approval gate before production deployments
- Unit tests wired into the pipeline as a test stage
- Tighter IAM policies scoped to least privilege

---

## Setup

### Prerequisites
- AWS account with a non-root IAM user configured
- AWS CLI installed and configured (`aws configure`)
- SAM CLI installed
- GitHub account

### Deploy

Clone the repository:
```bash
git clone git@github.com:YOUR_USERNAME/lambda-pipeline-demo.git
cd lambda-pipeline-demo
```

The pipeline handles all deployments automatically on push to `main`. To trigger a manual deployment locally:
```bash
sam build
sam deploy --stack-name lambda-pipeline-demo \
  --s3-bucket YOUR_ARTIFACT_BUCKET \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```

---

## Usage

### Create an item
```bash
curl -X POST "https://YOUR_API_URL/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Item"}'
```

### Get all items
```bash
curl "https://YOUR_API_URL/items"
```

### Get a single item
```bash
curl "https://YOUR_API_URL/items/{id}"
```

### Delete an item
```bash
curl -X DELETE "https://YOUR_API_URL/items/{id}"
```

---

## Free Tier Coverage

This project operates entirely within the AWS free tier at normal usage:

| Service | Free Tier Limit |
|---|---|
| Lambda | 1M requests/month |
| API Gateway | 1M requests/month |
| DynamoDB | 25GB storage, 200M requests/month |
| CodeBuild | 100 build minutes/month |
| CodePipeline | 1 free pipeline/month |
| S3 | 5GB storage |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
