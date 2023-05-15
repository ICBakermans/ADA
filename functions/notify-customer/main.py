import functions_framework
from flask import jsonify, request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from python_http_client.exceptions import HTTPError
from google.cloud import bigquery

# Create a BigQuery client
bigquery_client = bigquery.Client()

def get_customer_details(customer_id):
    """
    Get the email address of a customer by customer_id
    """
    query = """
    SELECT mail, first_name
    FROM goodsgriddb.customer_data
    WHERE customer_id = {}
    """.format(customer_id)

    query_job = bigquery_client.query(query)
    result = query_job.result()
    email, first_name = [(row.mail, row.first_name) for row in result][0]
    return email, first_name


def send_email(customer_id, order_id):
    sg = SendGridAPIClient(os.environ['EMAIL_API_KEY'])

    customer_email, customer_first_name = get_customer_details(customer_id)

    html_content = "<p>Hello {}, your order with order id {} is on its way!</p>".format(customer_first_name, order_id)

    message = Mail(
        to_emails=customer_email,
        from_email=Email('l.m.v.kempen@student.tue.nl', "GoodsGrid"),
        subject="Order update",
        html_content=html_content
        )
    message.add_bcc("l.m.v.kempen@student.tue.nl")

    try:
        response = sg.send(message)
        return f"Email sent successfully, status_code={response.status_code}"
    except HTTPError as e:
        return f"Failed to send email: {e.message}"

@functions_framework.http
def notify_customer(request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    request_json = request.get_json()

    if not request_json or 'input' not in request_json:
        return jsonify({'error': 'Invalid request data'}), 400

    input_data = request_json['input']

    if not isinstance(input_data, list) or not all(isinstance(item, dict) for item in input_data):
        return jsonify({'error': 'Invalid input data'}), 400

    customer_notifications = []
    for item in input_data:
        if 'customer_id' in item and 'order_id' in item:
            send_email(item['customer_id'], item['order_id'])
            customer_notifications.append({
                'customer_id': item['customer_id'],
                'order_id': item['order_id'],
            })

    if not customer_notifications:
        return jsonify({'message': 'No customers to notify'}), 200

    notification_message = {
        'message': 'The following customers have been notified that their order is on the way',
        'notifications': customer_notifications
    }

    return jsonify(notification_message), 200
