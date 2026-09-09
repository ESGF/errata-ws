import re

import tornado

from errata_ws import db
from errata_ws import notifications
from errata_ws.utils import constants
from errata_ws.utils import exceptions
from errata_ws.utils import http_security
from errata_ws.utils.http import process_request
from errata_ws.utils.publisher import get_entities_on_errata_propose
from errata_ws.utils.validation import validate_url, validate_dataset_id


class ProposeErrataRequestHandler(tornado.web.RequestHandler):
    """Propose errata handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        http_security.set_headers(self, True)


    def options(self):
        """HTTP OPTIONS handler.

        """
        self.set_status(204)
        self.set_default_headers()
        self.finish()


    def post(self):
        """HTTP POST handler.

        """
        def _validate_issue_datasets():
            """Validates datasets associated with incoming issue.

            """
            # Exception if no usable dataset identifiers.
            sanitized_datasets = [
                dset.encode('ascii', 'ignore').decode('ascii')
                for dset in self.request.data[constants.JF_DATASETS]
                ]
            if sanitized_datasets is None or len(sanitized_datasets) == 0:
                raise exceptions.EmptyDatasetList()

            # Exception if dataset version is missing.
            for dset in sanitized_datasets:
                if re.search(constants.VERSION_REGEX, dset) is None:
                    raise exceptions.MissingVersionNumber(dset)

                # Exception if esgvoc dataset parsing fails.
                validate_dataset_id(self.request.data[constants.JF_PROJECT], dset.split("#")[0])


        def _validate_issue_title():
            """Validates URL's associated with incoming request.

            """
            # Exception if duplicate title.
            issue_title = self.request.data[constants.JF_TITLE]
            with db.session.create():
                existing_titles = db.dao.get_titles()
                if issue_title in existing_titles:
                    raise exceptions.TitleExistsError(issue_title)


        def _validate_issue_urls():
            """Validates URL's associated with incoming request.

            """
            # Exception if an associated issue URL is invalid.
            urls = self.request.data[constants.JF_URLS] + self.request.data[constants.JF_MATERIALS]
            urls = [i for i in urls if i]
            for url in urls:
                validate_url(url)


        def _persist():
            """Persists data to dB.

            """
            with db.session.create(commitable=True):
                # Map request data to db entities.
                entities = get_entities_on_errata_propose(self.request.data, self.request.data["userEmail"])

                # Insert errata.
                db.session.insert(entities[0], auto_commit=False)

                # Insert associated entities (facets/resources/pid-tasks).
                for entity in entities[1:]:
                    db.session.insert(entity, auto_commit=False)
                
                # Make available downstream.
                self.issue_created_by = entities[0].created_by
                self.issue_uid = entities[0].uid
                self.issue_institute = entities[0].institute



        def _notify():
            """Notifies proposer & moderation team.

            """
            notifications.dispatch_on_proposed_1(
                self.request.protocol,
                self.request.host,
                self.issue_created_by,
                self.issue_uid
            )
            # notifications.dispatch_on_proposed_2(
            #     self.request.protocol,
            #     self.request.host,
            #     self.issue_created_by,
            #     self.issue_uid,
            #     self.issue_institute
            # )
            notifications.dispatch_on_proposed_3(
                self.request.protocol,
                self.request.host,
                self.issue_created_by,
                self.issue_uid,
            )


        # Process request.
        process_request(self, [
            _validate_issue_title,
            _validate_issue_datasets,
            _validate_issue_urls,
            _persist,
            _notify
        ])
