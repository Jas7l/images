import flask

from base_module.base_models import ModuleException
from base_module.base_models import setup_logging
from base_module.services import TracingService
from config import config
from injectors.connections import pg
from routers.tasks import images_bp


def setup_app():
    current = flask.Flask(__name__)
    pg.setup(current)
    TracingService.setup_flask_tracing(current)
    setup_logging(config.logging)

    return current


app = setup_app()
app.register_blueprint(images_bp)


@app.errorhandler(ModuleException)
def handle_exception(error: ModuleException):
    response = flask.jsonify(error.json())
    response.status_code = error.code
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
