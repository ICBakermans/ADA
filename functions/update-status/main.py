import functions_framework
from google.cloud import bigquery
from datetime import datetime
from flask import jsonify

# Create a BigQuery client
bigquery_client = bigquery.Client()

@functions_framework.http
def update_status(request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    # Get the current datetime
    current_datetime = datetime.now()

    # Define the query to get the customer_id and order_id of rows where status is 'payment_pending'
    select_query = """
    SELECT customer_id, order_id
    FROM goodsgriddb.payment_data
    WHERE status = 'payment_pending'
    """

    # Execute the select query
    select_job = bigquery_client.query(select_query)

    # Get the result of the query and store it in a list
    results = select_job.result()
    rows_to_update = [{'customer_id': row.customer_id, 'order_id': row.order_id} for row in results]

    # Define the query to update the status
    update_query = """
    UPDATE `goodsgriddb.payment_data`
    SET status = 'payment_completed', updated_at = '{}'
    WHERE status = 'payment_pending'
    AND customer_id = 26
    """.format(current_datetime)

    # Execute the update query
    update_job = bigquery_client.query(update_query)

    # Wait for the update query to complete
    update_job.result()

    # Return a JSON response with the list of rows that were updated
    return jsonify(rows_to_update)
