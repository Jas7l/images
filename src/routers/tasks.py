from flask import Blueprint, jsonify, request

from injectors import services

images_bp = Blueprint('images', __name__, url_prefix='/api')

@images_bp.route('/images', methods=['POST'])
def create_image():
    ts = services.tasks_service()
    res = ts.create_task(request.json)
    return jsonify(res)

@images_bp.route('/images', methods=['GET'])
def get_images():
    ts = services.tasks_service()
    ts.get_all()
    return jsonify(ts.get_all())


@images_bp.route('/images/<int:task_id>', methods=['GET'])
def get_image(task_id):
    ts = services.tasks_service()
    ts.get(task_id)
    return jsonify(ts.get(task_id))