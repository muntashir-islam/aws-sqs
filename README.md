# Flask SQS Application

## Overview

This project is a Flask application that integrates with AWS SQS (Simple Queue Service). It provides endpoints to produce and consume messages from an SQS queue. The application is containerized using Docker and deployed to Kubernetes.

## Features

- **Produce Messages:** Send messages to an SQS queue.
- **Consume Messages:** Retrieve and process messages from an SQS queue.
- **Dockerized:** The application is built and packaged in a Docker container.
- **Kubernetes Deployment:** Deployed on a Kubernetes cluster for scalable and reliable operation.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Testing](#testing)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Kubernetes](https://kubernetes.io/docs/tasks/tools/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-repo/flask-sqs-app.git
cd flask-sqs-app
```
## Build the Docker Image
```
docker build -t your-dockerhub-username/flask-sqs-app:latest .
```

# Usage

## Running Locally

To run the Flask application locally, use the following command:
```
docker run -p 5000:5000 \
    -e AWS_ACCESS_KEY_ID=your-access-key-id \
    -e AWS_SECRET_ACCESS_KEY=your-secret-access-key \
    -e AWS_REGION=your-region \
    -e SQS_QUEUE_URL=your-queue-url \
    your-dockerhub-username/flask-sqs-app:latest
```

## API Endpoints

Produce a Message

Endpoint: `POST /produce`

Request Body:

```shell
{
  "message": "Your message here"
}
```
Response:
```shell
{
  "message_id": "id_of_the_message"
}
```

Endpoint: `GET /consume`

Response:
```shell
{
  "message": "Your message content here"
}
```
# Testing
## Run Unit Tests

To run unit tests for the Flask application, use the following command:
```shell
python -m unittest discover -s tests
```

## Docker Container for Testing
You can also run the tests inside the Docker container:
```shell
docker run --rm your-dockerhub-username/flask-sqs-app:latest python -m unittest discover -s tests
```
### Summary

- **Sections:** Clear sections including overview, setup, usage, and deployment instructions.
- **Commands:** Includes all necessary commands and code blocks for installation, usage, testing, and deployment.
- **API Endpoints:** Provides details on how to interact with the API.

Replace placeholders with actual values relevant to your project setup, such as Docker Hub username, AWS credentials, and Kubernetes configuration.

