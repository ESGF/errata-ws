import re

import tornado

from errata_ws import db
from errata_ws.utils import config
from errata_ws.utils import constants
from errata_ws.utils import exceptions
from errata_ws.utils import http_security
from errata_ws.utils.http import process_request
from errata_ws.utils.publisher import get_institute
from errata_ws.utils.publisher import get_entities_on_errata_update
from errata_ws.utils.publisher import get_pid_tasks_on_errata_update
from errata_ws.utils.http_security import authorize
from errata_ws.utils.validation import validate_url, validate_dataset_id


def persist_errata_update(issue, obj, user_id, user_role):
    """Persist an errata update and its PID tasks in the active transaction."""
    datasets_old = db.dao.get_datasets(issue.uid)

    db.dao.delete_facets(issue.uid)
    db.dao.delete_resources(issue.uid)

    entities = get_entities_on_errata_update(issue, obj, user_id, user_role)
    for entity in entities:
        db.session.insert(entity, auto_commit=False)

    datasets_new = set(obj[constants.JF_DATASETS])
    tasks = get_pid_tasks_on_errata_update(issue.uid, datasets_old, datasets_new)
    for task in tasks:
        db.session.insert(task, auto_commit=False)


class UpdateErrataRequestHandler(tornado.web.RequestHandler):
    """Publishing update issue handler.

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
            sanitized_datasets = [dt.strip().encode('ascii', 'ignore').decode('ascii')
                                  for dt in self.request.data[constants.JF_DATASETS]]
            if sanitized_datasets is None or sanitized_datasets == 0:
                raise exceptions.EmptyDatasetList()
            else:
                for dset in sanitized_datasets:
                    if re.search(constants.VERSION_REGEX, dset) is None:
                        raise exceptions.MissingVersionNumber(dset)
                    validate_dataset_id(self.request.data[constants.JF_PROJECT], dset)


        def _validate_user_access():
            """Validates user's institutional access rights.

            """
            if config.apply_security_policy:
                self.user_role = authorize(
                    self.user_id, 
                    self.request.data[constants.JF_PROJECT], 
                    get_institute(self.request.data)
                    )
            else:
                self.user_role = None


        def _validate_issue_exists():
            """Validates that the issue has been previously posted to the web-service.

            """
            self.issue = db.dao.get_issue(self.request.data[constants.JF_UID])
            if self.issue is None:
                raise exceptions.UnknownIssueError(self.request.data[constants.JF_UID])


        def _validate_issue_urls():
            """Validates URL's associated with incoming request.

            """
            urls = self.request.data[constants.JF_URLS] + self.request.data[constants.JF_MATERIALS]
            urls = [i for i in urls if i]
            for url in urls:
                validate_url(url)


        def _validate_issue_immutable_attributes():
            """Validates that issue attribute deemed to be immutable have not been changed.

            """
            # if self.issue.institute != get_institute(self.request.data):
            #     raise exceptions.IssueImmutableAttributeError('institute')
            for attr in constants.ISSUE_IMMUTABLE_ATTRIBUTES:
                if self.request.data[attr].lower() != getattr(self.issue, attr).lower():
                    raise exceptions.IssueImmutableAttributeError(attr)


        def _validate_issue_status():
            """Validates that issue status allows it to be updated.

            """
            if self.issue.status != constants.ISSUE_STATUS_NEW and self.request.data[constants.JF_STATUS] == constants.ISSUE_STATUS_NEW:
                raise exceptions.IssueStatusChangeError()


        def _persist():
            """Persists data to dB.

            """
            # The surrounding commitable session performs the single commit;
            # PID dispatch itself remains asynchronous.
            persist_errata_update(
                self.issue,
                self.request.data,
                self.user_id,
                self.user_role
            )


        def _notify_on_moderation():
            """Dispatches moderation notifications.

            """
            print(666)


        # Process request.
        with db.session.create(commitable=True):
            process_request(self, [
                _validate_issue_datasets,
                _validate_user_access,
                _validate_issue_exists,
                _validate_issue_urls,
                _validate_issue_immutable_attributes,
                _validate_issue_status,
                _persist,
                _notify_on_moderation
            ])
