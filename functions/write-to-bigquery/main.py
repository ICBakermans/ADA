import functions_framework
from flask import jsonify, request
from google.cloud import bigquery
from datetime import datetime
import random
import string

# Create a BigQuery client
bigquery_client = bigquery.Client()


@functions_framework.http
def create_payment(request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    payment_data = request.get_json()

    if not payment_data:
        return jsonify({'error': 'Invalid payment data'}), 400

    # Perform validation checks on the payment data
    if 'amount' not in payment_data or 'customer_id' not in payment_data:
        return jsonify({'error': 'Payment data is missing required fields'}), 400

    if payment_data['amount'] <= 0:
        return jsonify({'error': 'Invalid payment amount'}), 400

    # Store the payment information in BigQuery
    dataset_id = 'goodsgriddb'
    table_id = 'payment_data'

    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Get the table
    table = bigquery_client.get_table(table_ref)

    # Get the maximum order_id
    query = """
    SELECT MAX(order_id) AS max_order_id
    FROM goodsgriddb.payment_data
    """
    query_job = bigquery_client.query(query)
    result = query_job.result()
    max_order_id = [row.max_order_id for row in result][0]
    new_order_id = int(max_order_id) + 1

    # Get the current datetime
    current_datetime = datetime.now()

    def generate_unique_id():
        current_time = datetime.now().strftime("%f")
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        unique_id = current_time + random_string
        return unique_id[:10]

    def is_unique(unique_id):
        query = """
        SELECT COUNT(*) AS count
        FROM goodsgriddb.payment_data
        WHERE payment_id = '{}'
        """.format(unique_id)

        query_job = bigquery_client.query(query)
        result = query_job.result()
        count = [row.count for row in result][0]

        return count == 0

    def get_unique_payment_id():
        unique_payment_id = generate_unique_id()

        while not is_unique(unique_payment_id):
            unique_payment_id = generate_unique_id()

        return unique_payment_id

    unique_payment_id = get_unique_payment_id()

    row_to_insert = (
        payment_data['customer_id'],
        payment_data['amount'],
        "payment_pending",  # Set the status as "payment_pending"
        unique_payment_id,  # Set the payment_id as an unique_payment_id through three methods
        current_datetime,  # Set the created_at with the current datetime
        current_datetime,  # Set the updated_at with the current datetime
        new_order_id  # Set the order_id as the incremented max_order_id
    )

    errors = bigquery_client.insert_rows(table, [
        row_to_insert])  # The schema is already defined in the table. You don't need to pass it here.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

    # Return a success response
    return jsonify({'message': 'Payment created successfully'}), 200
