import unittest
from unittest.mock import patch, MagicMock
from app import app


class FlaskSqsAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.sqs.send_message')
    def test_produce_message(self, mock_send_message):
        # Define a mock response for send_message
        mock_send_message.return_value = {'MessageId': '12345'}

        # Test producing a message
        response = self.app.post('/produce', json={'message': 'Hello, SQS!'})

        # Check the status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertIn('message_id', response.json)
        self.assertEqual(response.json['message_id'], '12345')

        # Verify that send_message was called once
        mock_send_message.assert_called_once_with(
            QueueUrl='your-queue-url',
            MessageBody='Hello, SQS!'
        )

    @patch('app.sqs.receive_message')
    @patch('app.sqs.delete_message')
    def test_consume_message(self, mock_delete_message, mock_receive_message):
        # Define a mock response for receive_message
        mock_receive_message.return_value = {
            'Messages': [
                {
                    'Body': 'Hello, SQS!',
                    'ReceiptHandle': 'abc123'
                }
            ]
        }

        # Test consuming a message
        response = self.app.get('/consume')

        # Check the status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Hello, SQS!')

        # Verify that receive_message was called once
        mock_receive_message.assert_called_once_with(
            QueueUrl='your-queue-url',
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )

        # Verify that delete_message was called once
        mock_delete_message.assert_called_once_with(
            QueueUrl='your-queue-url',
            ReceiptHandle='abc123'
        )

    @patch('app.sqs.receive_message')
    def test_consume_message_empty_queue(self, mock_receive_message):
        # Define a mock response with no messages
        mock_receive_message.return_value = {
            'Messages': []
        }

        # Test consuming a message from an empty queue
        response = self.app.get('/consume')

        # Check the status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'No messages in queue')

        # Verify that receive_message was called once
        mock_receive_message.assert_called_once_with(
            QueueUrl='your-queue-url',
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )


if __name__ == '__main__':
    unittest.main()
