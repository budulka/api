from flask import request

def get_request_data():
    """
    Get keys & values from request. Handles both "application/x-www-form-urlencoded" and "application/json".
    Returns data as a dictionary.
    """
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    elif request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = {}
    return data

