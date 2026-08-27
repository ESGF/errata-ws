from unittest import mock

from errata_ws.utils import constants
from errata_ws.handlers.publication import update
from errata_ws.utils.publisher import get_pid_tasks_on_errata_update


_ISSUE_UID = u'4c5dd574-f9bb-4e04-b9a7-d731c7327a0d'


def _as_tuples(tasks):
    return [(task.action, task.dataset_id, task.issue_uid) for task in tasks]


def test_metadata_only_update_creates_no_pid_tasks():
    datasets = {u'CMIP6.example#20200101'}

    tasks = get_pid_tasks_on_errata_update(_ISSUE_UID, datasets, datasets)

    assert tasks == []


def test_added_dataset_creates_only_insert_task():
    existing = u'CMIP6.existing#20200101'
    added = u'CMIP6.added#20200102'

    tasks = get_pid_tasks_on_errata_update(_ISSUE_UID, {existing}, {existing, added})

    assert _as_tuples(tasks) == [(constants.PID_ACTION_INSERT, added, _ISSUE_UID)]


def test_removed_dataset_creates_only_delete_task():
    retained = u'CMIP6.retained#20200101'
    removed = u'CMIP6.removed#20200102'

    tasks = get_pid_tasks_on_errata_update(_ISSUE_UID, {retained, removed}, {retained})

    assert _as_tuples(tasks) == [(constants.PID_ACTION_DELETE, removed, _ISSUE_UID)]


def test_added_and_removed_datasets_create_deterministic_tasks():
    tasks = get_pid_tasks_on_errata_update(
        _ISSUE_UID,
        {u'CMIP6.remove-b#20200102', u'CMIP6.keep#20200101', u'CMIP6.remove-a#20200101'},
        {u'CMIP6.add-b#20200102', u'CMIP6.keep#20200101', u'CMIP6.add-a#20200101'}
    )

    assert _as_tuples(tasks) == [
        (constants.PID_ACTION_DELETE, u'CMIP6.remove-a#20200101', _ISSUE_UID),
        (constants.PID_ACTION_DELETE, u'CMIP6.remove-b#20200102', _ISSUE_UID),
        (constants.PID_ACTION_INSERT, u'CMIP6.add-a#20200101', _ISSUE_UID),
        (constants.PID_ACTION_INSERT, u'CMIP6.add-b#20200102', _ISSUE_UID)
    ]


def test_update_and_pid_tasks_are_staged_without_an_inner_commit():
    issue = mock.Mock(uid=_ISSUE_UID)
    obj = {constants.JF_DATASETS: [u'CMIP6.added#20200102']}
    issue_entities = [mock.sentinel.resource, mock.sentinel.facet]
    pid_tasks = [mock.sentinel.pid_task]

    with mock.patch.object(update.db.dao, 'get_datasets', return_value=set()), \
            mock.patch.object(update.db.dao, 'delete_facets'), \
            mock.patch.object(update.db.dao, 'delete_resources'), \
            mock.patch.object(update, 'get_entities_on_errata_update', return_value=issue_entities), \
            mock.patch.object(update, 'get_pid_tasks_on_errata_update', return_value=pid_tasks), \
            mock.patch.object(update.db.session, 'insert') as insert:
        update.persist_errata_update(issue, obj, 'publisher', constants.USER_ROLE_AUTHOR)

    assert insert.call_args_list == [
        mock.call(mock.sentinel.resource, auto_commit=False),
        mock.call(mock.sentinel.facet, auto_commit=False),
        mock.call(mock.sentinel.pid_task, auto_commit=False)
    ]


def test_update_persistence_does_not_commit_the_active_transaction():
    issue = mock.Mock(uid=_ISSUE_UID)
    obj = {constants.JF_DATASETS: []}

    with mock.patch.object(update.db.dao, 'get_datasets', return_value=set()), \
            mock.patch.object(update.db.dao, 'delete_facets'), \
            mock.patch.object(update.db.dao, 'delete_resources'), \
            mock.patch.object(update, 'get_entities_on_errata_update', return_value=[]), \
            mock.patch.object(update, 'get_pid_tasks_on_errata_update', return_value=[]), \
            mock.patch.object(update.db.session, 'insert'), \
            mock.patch.object(update.db.session, 'commit') as commit:
        update.persist_errata_update(issue, obj, 'publisher', constants.USER_ROLE_AUTHOR)

    commit.assert_not_called()
