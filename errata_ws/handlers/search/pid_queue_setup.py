import tornado

from errata_ws.utils import constants
from errata_ws.utils.http import process_request
from errata_ws.utils.mapper import map_collection


class PIDQueueSearchSetupRequestHandler(tornado.web.RequestHandler):
    """Search PID queue request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """
        def _set_output():
            """Sets response to be returned to client.

            """
            # Set vocabs to be loaded.
            vocabs = [
                'project',
                'pid-task-action',
                'pid-task-status'
            ]

            # Set output.
            self.output = {
                'vocabs': [map_collection(i) for i in vocabs],
            }

        # Process request.
        process_request(self, _set_output)
