import tornado

from errata_ws.utils.validation import validate_dataset_id
from errata_ws.utils.http import process_request


# Query parameter names.
_PARAM_PROJECT = 'project'
_PARAM_IDENTIFIER = 'identifier'


class ValidateDatasetIdentifierRequestHandler(tornado.web.RequestHandler):
    """Exposes dataset id validation method.

    """
    def get(self):
        """HTTP GET handler.

        """
        def _validate():
            """
            Validates dataset identifer using esgvoc.
            """

            validate_dataset_id(self.get_argument(_PARAM_PROJECT), self.get_argument(_PARAM_IDENTIFIER))


        def _set_output():
            """Sets response to be returned to client.

            """
            self.output = {
                "message": "Dataset identifier is valid:: project={}; id={}.".format(
                    self.get_argument(_PARAM_PROJECT), self.get_argument(_PARAM_IDENTIFIER))
            }


        # Process request.
        process_request(self, [
            _validate,
            _set_output
            ])
