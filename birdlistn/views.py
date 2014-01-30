"""
URL routes declarations.

All views are currently declared here.

"""
import os

from flask import jsonify

from birdlistn import app, make_json_error, listener
from cloudly import logger

log = logger.init(__name__)


@app.errorhandler(Exception)
def error_handler(error):
    return make_json_error(error)


@app.route('/')
def index():
    """ Return the status of the listener.
    """
    return jsonify(status={'running': listener.is_running})


@app.route('/start')
def start():
    log.debug("Starting listener")
    listener.start()
    return jsonify(status={'running': listener.is_running})


@app.route('/stop')
def stop():
    log.debug("Stopping listener.")
    listener.stop(True)
    return jsonify(status={'running': listener.is_running})


def in_production():
    return os.environ.get("IS_PRODUCTION", "").lower() in ['true', 'yes']
