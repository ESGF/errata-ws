import esgvoc.api as ev
import tornado

from errata_ws import db
from errata_ws.utils import http_security
from errata_ws.utils.http import process_request
from errata_ws.utils.mapper import map_collection


class SearchErrataSetupRequestHandler(tornado.web.RequestHandler):
    """Search issue request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        http_security.set_headers(self)


    def get(self):
        """HTTP GET handler.

        """
        def _set_output():
            """Sets response to be returned to client.

            """
            # Set vocabs to be loaded.
            vocabs = {
                'esdoc:errata:project',
                'esdoc:errata:severity',
                'esdoc:errata:status',
                'esdoc:errata:moderation-status'
            }

            for project in ev.get_all_projects():
                collections = ev.get_all_collections_in_project(project)
                for collection in collections:
                    vocabs.add(f"wcrp:{project}:{collection}")

            # Get facet values.
            with db.session.create():
                facet_values = list(set(db.dao.get_project_facets()))

            # Set output.
            self.output = {
                'vocabs': [map_collection(i) for i in sorted(vocabs)],
                'values': facet_values
            }

        # Process request.
        process_request(self, _set_output)
