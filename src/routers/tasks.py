from flask import (
    Blueprint,
    jsonify,
    request
)

from injectors import services

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api')


@tasks_bp.route('/tasks', methods=['POST'])
def create_image():
    ts = services.tasks_service()
    res = ts.create_task(request.json)
    return jsonify(res)


@tasks_bp.route('/tasks', methods=['GET'])
def get_images():
    ts = services.tasks_service()
    ts.get_all()
    return jsonify(ts.get_all())


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_image(task_id):
    ts = services.tasks_service()
    ts.get(task_id)
    return jsonify(ts.get(task_id))
