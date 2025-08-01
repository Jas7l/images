import typing as t
from uuid import uuid4

import flask
import requests as r

from ..base_models import ClassesLoggerAdapter


class TracingService:
    """."""

    TRACE_HEADER = 'X-Trace-Id'

    @classmethod
    def tracing_request(cls):
        trace_id = flask.request.headers.get(cls.TRACE_HEADER)
        trace_id = trace_id or uuid4().hex
        ClassesLoggerAdapter.TRACE_ID.set(trace_id)

    @classmethod
    def tracing_response(cls, response: flask.Response) -> flask.Response:
        cls.set_trace_id(response)
        return response

    @classmethod
    def set_trace_id(cls, ro: t.Union[r.Request, r.Session, flask.Response]):
        ro.headers[cls.TRACE_HEADER] = ClassesLoggerAdapter.TRACE_ID.get()

    @classmethod
    def setup_flask_tracing(cls, app: flask.Flask):
        app.before_request(TracingService.tracing_request)
        app.after_request(TracingService.tracing_response)
