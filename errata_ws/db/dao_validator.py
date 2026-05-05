from errata_ws.utils import constants
from errata_ws.utils import validation as v



def validate_delete_facets(issue_uid):
    """Function input validator: delete_facets.

    """
    v.validate_uid(issue_uid, 'Issue unique identifier')


def validate_delete_resources(issue_uid):
    """Function input validator: delete_resources.

    """
    v.validate_uid(issue_uid, 'Issue unique identifier')


def validate_get_datasets(issue_uid):
    """Function input validator: get_datasets.

    """
    v.validate_uid(issue_uid, 'Issue unique identifier')


def validate_get_issue(uid):
    """Function input validator: get_issue.

    """
    v.validate_uid(uid, 'Issue unique identifier')


def validate_get_resources(issue_uid=None):
    """Function input validator: get_resources.

    """
    if issue_uid is not None:
        v.validate_uid(issue_uid, 'Issue unique identifier')
