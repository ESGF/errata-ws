import json

import jsonschema

from errata_ws.utils import exceptions
from errata_ws.schemas import get_schema


def clean_data(data: dict[str, str | bytes | list[bytes | str]]) -> dict[str, str | list[str]]:
    result: dict[str, str | list[str]] = {}

    for key, values in data.items():
        if isinstance(values, list):
            cleaned_values: list[str] = []
            for value in values:
                if isinstance(value, bytes):
                    cleaned_values.append(value.decode())
                else:
                    cleaned_values.append(value)
        elif isinstance(values, bytes):
            cleaned_values = values.decode()
        else:
            cleaned_values = values

        result[key] = cleaned_values

    return result


def validate_request(handler):
    """Validates request against mapped JSON schemas.

    :param utils.http.HTTPRequestHandler handler: An HTTP request handler.

    :raises: exceptions.InvalidJSONError

    """
    for func in {
        _validate_request_headers,
        _validate_request_params,
        _validate_request_body,
    }:
        func(handler)


def _validate_request_headers(handler):
    """
    Validates request headers against a JSON schema.
    """
    # Map request to schema.
    schema = get_schema("headers", handler.request.path)

    # Null case - escape.
    if schema is None:
        return

    # Validate request headers.
    _validate(handler, dict(handler.request.headers), schema)


def _validate_request_params(handler):
    """
    Validates request parameters against a JSON schema.
    """
    # Map request to schema.
    schema = get_schema("params", handler.request.path)

    # Null case.
    if schema is None:
        if handler.request.query_arguments:
            raise exceptions.RequestValidationException(
                "Unexpected request url parameters."
            )

    # Validate request parameters.
    else:
        _validate(handler, handler.request.query_arguments, schema)


def _validate_request_body(handler):
    """
    Validates request body against a JSON schema.
    """
    # Map request to schema.
    schema = get_schema("body", handler.request.path)

    # Null case.
    if schema is None:
        if handler.request.body:
            raise exceptions.RequestValidationException("Unexpected request body.")

    # Validate request data.
    else:
        # ... decode request data.
        data = json.loads(handler.request.body)

        # ... validate request data against schema.
        _validate(handler, data, schema)

        # ... append valid data to request.
        handler.request.data = data


def _validate(handler, data: dict[str, list[bytes | str] | str], schema: dict):
    """
    Validates data against a JSON schema.
    """
    try:
        jsonschema.validate(clean_data(data), schema)
    except jsonschema.exceptions.ValidationError as err:
        raise exceptions.InvalidJSONError(err)
