import functions_framework
from flask import jsonify, request

@functions_framework.http
def notify_shipment(request):
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

    # Perform validation checks on the input data
    if not isinstance(input_data, list) or not all(isinstance(item, dict) for item in input_data):
        return jsonify({'error': 'Invalid input data'}), 400

    orders_to_ship = []
    for item in input_data:
        if 'customer_id' in item and 'order_id' in item:
            orders_to_ship.append(item['order_id'])

    if not orders_to_ship:
        return jsonify({'message': 'No orders to ship'}), 200

    # Create a shipment message
    shipment_message = {
        'message': 'The shipment can be started for the following orders',
        'orders': orders_to_ship
    }

    return jsonify(shipment_message), 200
