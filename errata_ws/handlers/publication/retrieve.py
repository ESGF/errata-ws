import tornado
from datetime import datetime

from errata_ws import db
from errata_ws.utils import constants
from errata_ws.utils.http import process_request



# Query parameter names.
_PARAM_UID = 'uid'


def _serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize(v) for v in obj]
    else:
        return obj


class RetrieveErrataRequestHandler(tornado.web.RequestHandler):
    """Publishing retrieve issue handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Headers", "content-type, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'GET')


    def get(self):
        """HTTP GET handler.

        """
        def _set_data():
            """Pulls data from db.

            """
            with db.session.create():
                self.issue = db.dao.get_issue(self.get_argument(_PARAM_UID))
                self.resources = db.dao.get_resources(issue_uid=self.get_argument(_PARAM_UID))
                self.facets = db.dao.get_facets(issue_uid=self.get_argument(_PARAM_UID))


        def _set_output():
            """Sets response to be returned to client.

            """
            raw_output = {
                'issue': self.issue.to_dict(self.resources, self.facets)
            }

            self.output = _serialize(raw_output)

        # Process request.
        process_request(self, [
            _set_data,
            _set_output
            ])
