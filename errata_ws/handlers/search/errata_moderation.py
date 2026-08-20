import tornado

from errata_ws import db
from errata_ws.utils import http_security
from errata_ws.utils.http import process_request



# Query parameters.
_PARAM_CRITERIA = 'criteria'


class SearchErrataModerationRequestHandler(tornado.web.RequestHandler):
    """Search issue for moderation request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        http_security.set_headers(self)


    def get(self):
        """HTTP GET handler.

        """
        def _set_criteria():
            """Sets search criteria.

            """
            self.criteria = {
                key: self.get_argument(key)
                for key in self.request.arguments
            }


        def _set_data():
            """Pulls data from db.

            """
            with db.session.create():
                print("CRIT MOD", self.criteria)
                rows = db.dao.get_issues(self.criteria, False)
                # Convert rows to dictionaries, ensuring all fields are included
                self.issues = [
                    {
                        'project': row[0],
                        'institute': row[1],
                        'uid': row[2],
                        'title': row[3],
                        'severity': row[4],
                        'status': row[5],
                        'dateCreated': row[6],
                        'dateUpdated': row[7],
                        'moderation_status': row[9]
                    }
                    for row in rows
                ]
                self.total = db.utils.get_count(db.models.Issue)


        def _set_output():
            """Sets response to be returned to client.

            """
            self.output = {
                'count': len(self.issues),
                'results': self.issues,
                'total': self.total
            }


        # Process request.
        process_request(self, [
            _set_criteria,
            _set_data,
            _set_output
            ])
