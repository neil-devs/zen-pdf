from flask import Blueprint, jsonify
from celery.result import AsyncResult

# Create the Blueprint (The "Module")
api_bp = Blueprint('api', __name__)

@api_bp.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    The Status Checker.
    Input: A Task ID (e.g., 'abc-123-xyz')
    Output: JSON status (Pending, Processing, Success, or Failure)
    """
    # 1. Look up the task in Redis using the ID
    task_result = AsyncResult(task_id)

    # 2. Build the response dictionary
    response = {
        'task_id': task_id,
        'status': task_result.status, # PENDING, STARTED, SUCCESS, FAILURE
        'result': None
    }

    # 3. If finished, include the result (e.g., filename) or error message
    if task_result.ready():
        if task_result.successful():
            response['result'] = task_result.result
        else:
            # If it failed, convert the error to a string so it sends safely
            response['result'] = str(task_result.result)

    # 4. Return as JSON (The "Burger" without the plate)
    return jsonify(response)