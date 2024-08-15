from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Get AWS credentials and SQS queue URL from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
sqs_queue_url = os.getenv('SQS_QUEUE_URL')

# Initialize the SQS client
sqs = boto3.client('sqs',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=aws_region)


# Producer: Send a message to the SQS queue
@app.route('/produce', methods=['POST'])
def produce_message():
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'Message content is required'}), 400

        response = sqs.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=message
        )

        return jsonify({'message_id': response['MessageId']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Consumer: Receive and process messages from the SQS queue
@app.route('/consume', methods=['GET'])
def consume_message():
    try:
        response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )

        messages = response.get('Messages', [])
        if not messages:
            return jsonify({'message': 'No messages in queue'})

        message_body = messages[0]['Body']

        # Delete the message from the queue after processing
        sqs.delete_message(
            QueueUrl=sqs_queue_url,
            ReceiptHandle=messages[0]['ReceiptHandle']
        )

        return jsonify({'message': message_body})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
