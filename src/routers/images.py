from flask import Blueprint, jsonify

from injectors import services

images_bp = Blueprint('images', __name__, url_prefix='/api')

@images_bp.route('/images', methods=['GET'])
def get_images():
    return