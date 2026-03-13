esdoc_map = {
    'esdoc:errata:moderation-status': {
        'canonical_name': 'moderation-status',
        'key': 'esdoc:errata:moderation-status',
        'label': 'Moderation Status',
        'namespace': 'esdoc:errata:moderation-status',
        'terms': [
            {
                'canonical_name': 'accepted',
                'key': 'esdoc:errata:moderation-status:accepted',
                'label': 'Accepted',
                'namespace': 'esdoc:errata:moderation-status:accepted',
                'color': '#00ff00'
            },
            {
                'canonical_name': 'in-review',
                'key': 'esdoc:errata:moderation-status:in-review',
                'label': 'In Review',
                'namespace': 'esdoc:errata:moderation-status:in-review',
                'color': '#ff9900'
            },
            {
                'canonical_name': 'not-required',
                'key': 'esdoc:errata:moderation-status:not-required',
                'label': 'Not Required',
                'namespace': 'esdoc:errata:moderation-status:not-required',
                'color': '#0c343d'
            },
            {
                'canonical_name': 'rejected',
                'key': 'esdoc:errata:moderation-status:rejected',
                'label': 'Rejected',
                'namespace': 'esdoc:errata:moderation-status:rejected',
                'color': '#38761d'
            }
        ]
    },
    'esdoc:errata:project': {
        'canonical_name': 'project',
        'key': 'esdoc:errata:project',
        'label': 'Project',
        'namespace': 'esdoc:errata:project',
        'terms': [
            {
                'canonical_name': 'cmip5',
                'key': 'esdoc:errata:project:cmip5',
                'label': 'CMIP5',
                'namespace': 'esdoc:errata:project:cmip5',
                'facets': ['wcrp:cmip5:institute', 'wcrp:cmip5:experiment', 'wcrp:cmip5:model', 'wcrp:cmip5:variable'],
                'is_documented': True,
                'is_pid_client': False
            },
            {
                'canonical_name': 'cmip6',
                'key': 'esdoc:errata:project:cmip6',
                'label': 'CMIP6',
                'namespace': 'esdoc:errata:project:cmip6',
                'facets': ['wcrp:cmip6:institution-id', 'wcrp:cmip6:experiment-id', 'wcrp:cmip6:source-id', 'wcrp:cmip6:variable-id'],
                'is_documented': True,
                'is_pid_client': True
            },
            {
                'canonical_name': 'cordex',
                'key': 'esdoc:errata:project:cordex',
                'label': 'CORDEX',
                'namespace': 'esdoc:errata:project:cordex',
                'facets': ['wcrp:cordex:institute', 'wcrp:cordex:experiment', 'wcrp:cordex:rcm-model', 'wcrp:cordex:variable'],
                'is_documented': False,
                'is_pid_client': False
            },
            {
                'canonical_name': 'input4mips',
                'key': 'esdoc:errata:project:input4mips',
                'label': 'input4MIPs',
                'namespace': 'esdoc:errata:project:input4mips',
                'facets': [
                    'wcrp:input4mips:target-mip',
                    'wcrp:input4mips:institution-id',
                    'wcrp:input4mips:source-id',
                    'wcrp:input4mips:variable-id'
                ],
                'is_documented': False,
                'is_pid_client': True
            }
        ]
    },
    'esdoc:errata:severity': {
        'canonical_name': 'severity',
        'key': 'esdoc:errata:severity',
        'label': 'Severity',
        'namespace': 'esdoc:errata:severity',
        'terms': [
            {
                'canonical_name': 'critical',
                'key': 'esdoc:errata:severity:critical',
                'label': 'Critical',
                'namespace': 'esdoc:errata:severity:critical',
                'color': '#a61c00',
                'sortOrdinal': 3
            },
            {
                'canonical_name': 'high',
                'key': 'esdoc:errata:severity:high',
                'label': 'High',
                'namespace': 'esdoc:errata:severity:high',
                'color': '#cc4125',
                'sortOrdinal': 2
            },
            {
                'canonical_name': 'low',
                'key': 'esdoc:errata:severity:low',
                'label': 'Low',
                'namespace': 'esdoc:errata:severity:low',
                'color': '#e6b8af',
                'sortOrdinal': 0
            },
            {
                'canonical_name': 'medium',
                'key': 'esdoc:errata:severity:medium',
                'label': 'Medium',
                'namespace': 'esdoc:errata:severity:medium',
                'color': '#dd7e6b',
                'sortOrdinal': 1
            }
        ]
    },
    'esdoc:errata:status': {
        'canonical_name': 'status',
        'key': 'esdoc:errata:status',
        'label': 'Status',
        'namespace': 'esdoc:errata:status',
        'terms': [
            {'canonical_name': 'new', 'key': 'esdoc:errata:status:new', 'label': 'New', 'namespace': 'esdoc:errata:status:new', 'color': '#00ff00'},
            {
                'canonical_name': 'onhold',
                'key': 'esdoc:errata:status:onhold',
                'label': 'On Hold',
                'namespace': 'esdoc:errata:status:onhold',
                'color': '#ff9900'
            },
            {
                'canonical_name': 'resolved',
                'key': 'esdoc:errata:status:resolved',
                'label': 'Resolved',
                'namespace': 'esdoc:errata:status:resolved',
                'color': '#0c343d'
            },
            {
                'canonical_name': 'wontfix',
                'key': 'esdoc:errata:status:wontfix',
                'label': 'Wont Fix',
                'namespace': 'esdoc:errata:status:wontfix',
                'color': '#38761d'
            }
        ]
    },
    "esdoc:errata:pid-task-action": {
        'key': 'esdoc:errata:pid-task-action',
        'label': 'Action',
        'terms': [
            {
                'canonical_name': 'delete',
                'key': 'esdoc:errata:pid-task-action:delete',
                'namespace': 'esdoc:errata:pid-task-action:delete',
                'label': 'Delete'
            },
            {
                'canonical_name': 'insert',
                'key': 'esdoc:errata:pid-task-action:insert',
                'namespace': 'esdoc:errata:pid-task-action:insert',
                'label': 'Insert'
            }
        ]
    },
    "esdoc:errata:pid-task-status": {
        'key': 'esdoc:errata:pid-task-status',
        'label': 'Status',
        'terms': [
            {
                'canonical_name': 'complete',
                'key': 'esdoc:errata:pid-task-status:complete',
                'namespace': 'esdoc:errata:pid-task-status:complete',
                'label': 'Complete',
                'color': '#e6b8af'
            },
            {
                'canonical_name': 'error',
                'key': 'esdoc:errata:pid-task-status:error',
                'namespace': 'esdoc:errata:pid-task-status:error',
                'label': 'Error',
                'color': '#a61c00'
            },
            {
                'canonical_name': 'queued',
                'key': 'esdoc:errata:pid-task-status:queued',
                'namespace': 'esdoc:errata:pid-task-status:queued',
                'label': 'Queued',
                'color': '#dd7e6b'
            }
        ]
    }
}