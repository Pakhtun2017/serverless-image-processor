Serverless Image Processor

Overview

**Serverless Image Processor** is a full-stack, serverless application for automatic image processing on AWS.  
- **Upload images** via a web form (Flask frontend coming soon!)
- Images are stored in S3 and automatically converted to thumbnails by a Lambda function (using Pillow)
- Thumbnail metadata is stored in DynamoDB
- Gallery page (Flask) will display all images and thumbnails



Architecture

User (Browser)
|
[Flask Web Frontend] <-- Coming soon!
|
[S3 Source Bucket] --> [Lambda (Pillow Layer)] --> [S3 Dest Bucket (Thumbnails)]
|
[DynamoDB Table]


CDK: 		All AWS resources are defined as code (Python)
Flask App:	Dockerized, deployed to EC2, communicates with AWS backend



Quick Start

Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured
- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
- Docker (for running CDK in containers)
- Python 3.11+
- An AWS account with necessary permissions

1. Clone the Repository

bash
git clone https://github.com/pakhtun2017/serverless-image-processor.git
cd serverless-image-processor


2. Install Python Dependencies
pip install -r requirements.txt


3. Bootstrapping, Synthesizing, and Deploying Infrastructure
You can manage AWS infrastructure in three ways:
	1) Directly via Docker
	2) Using the provided shell script
	3) Via Makefile targets

A) Using Docker Directly
	Bootstrap (set up environment for CDK):
		docker run --rm -it \
		  -e AWS_PROFILE=staging \
		  -v "$PWD":/app -w /app \
		  -v "$HOME/.aws":/root/.aws \
		  image-processor-cdk \
		  cdk bootstrap

	Synthesize (generate CloudFormation):
		docker run --rm -it \
		  -e AWS_PROFILE=staging \
		  -v "$PWD":/app -w /app \
		  -v "$HOME/.aws":/root/.aws \
		  image-processor-cdk \
		  cdk synth

	Deploy:
		docker run --rm -it \
		  -e AWS_PROFILE=staging \
		  -v "$PWD":/app -w /app \
		  -v "$HOME/.aws":/root/.aws \
		  image-processor-cdk \
		  cdk deploy --require-approval never

	Destroy (to delete all resources):
		docker run --rm -it \
		  -e AWS_PROFILE=staging \
		  -v "$PWD":/app -w /app \
		  -v "$HOME/.aws":/root/.aws \
		  image-processor-cdk \
		  cdk destroy --force


B) Using Shell Script
Use the provided helper script to simplify the above.
Example:
	./scripts/cdk-cmd.sh staging bootstrap
	./scripts/cdk-cmd.sh staging synth
	./scripts/cdk-cmd.sh staging deploy
	./scripts/cdk-cmd.sh staging destroy
You may customize the script to target other environments (e.g., dev, prod) as needed.


C) Using Makefile
You can also use common Makefile targets:
	make bootstrap ENV=staging
	make synth ENV=staging
	make deploy ENV=staging
	make destroy ENV=staging


4. Flask Frontend (Coming Soon!)
A Flask-based web frontend for image upload and gallery display will be added soon in flask-app/.

Will be fully Dockerized and ready to deploy on EC2/ECS/Beanstalk

Instructions will be added when available


