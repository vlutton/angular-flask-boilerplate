from flask import jsonify, url_for, current_app


class ValidationError(ValueError):
    pass

def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response
