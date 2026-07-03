metadata_mapper = {
    "project": {
        "key": "project",
        "label": "Project",
        "project": None,
        "terms": [
            {
                'canonical_name': 'cmip6',
                'key': 'cmip6',
                'label': 'CMIP6',
                'namespace': 'cmip6',
                'facets': ['institution_id', 'experiment_id', 'source_id', 'variable_id'],
                'is_documented': True,
                'is_pid_client': True
            },
            {
                'canonical_name': 'cmip7',
                'key': 'cmip7',
                'label': 'CMIP7',
                'namespace': 'cmip7',
                'facets': ['institution', 'experiment', 'source', 'variable'],
                'is_documented': True,
                'is_pid_client': True
            },
            {
                'canonical_name': 'cordex-cmip5',
                'key': 'cordex-cmip5',
                'label': 'CORDEX-CMIP5',
                'namespace': 'cordex-cmip5',
                'facets': ['institute', 'experiment', 'rcm-model', 'variable'],
                'is_documented': False,
                'is_pid_client': False
            },
            {
                'canonical_name': 'cordex-cmip6',
                'key': 'cordex-cmip6',
                'label': 'CORDEX-CMIP6',
                'namespace': 'cordex-cmip6',
                'facets': ['institute', 'experiment', 'rcm-model', 'variable'],
                'is_documented': False,
                'is_pid_client': False
            },
            {
                'canonical_name': 'input4mips',
                'key': 'input4mips',
                'label': 'input4MIPs',
                'namespace': 'input4mips',
                'facets': [
                    'target-mip',
                    'institution-id',
                    'source-id',
                    'variable-id'
                ],
                'is_documented': False,
                'is_pid_client': True
            }
        ]
    },
    "moderationStatus": {
        "key": "moderationStatus",
        "label": "Moderation status",
        "project": None,
        "terms": [
            {
                'canonical_name': 'accepted',
                'key': 'accepted',
                'label': 'Accepted',
                'namespace': 'accepted',
                'color': '#00ff00'
            },
            {
                'canonical_name': 'in-review',
                'key': 'in-review',
                'label': 'In Review',
                'namespace': 'in-review',
                'color': '#ff9900'
            },
            {
                'canonical_name': 'not-required',
                'key': 'not-required',
                'label': 'Not Required',
                'namespace': 'not-required',
                'color': '#0c343d'
            },
            {
                'canonical_name': 'rejected',
                'key': 'rejected',
                'label': 'Rejected',
                'namespace': 'rejected',
                'color': '#38761d'
            }
        ]
    },
    "severity": {
        "key": "severity",
        "label": "Severity",
        "project": None,
        "terms": [
            {
                'canonical_name': 'critical',
                'key': 'critical',
                'label': 'Critical',
                'namespace': 'critical',
                'color': '#a61c00',
                'sortOrdinal': 3
            },
            {
                'canonical_name': 'high',
                'key': 'high',
                'label': 'High',
                'namespace': 'high',
                'color': '#cc4125',
                'sortOrdinal': 2
            },
            {
                'canonical_name': 'low',
                'key': 'low',
                'label': 'Low',
                'namespace': 'low',
                'color': '#e6b8af',
                'sortOrdinal': 0
            },
            {
                'canonical_name': 'medium',
                'key': 'medium',
                'label': 'Medium',
                'namespace': 'medium',
                'color': '#dd7e6b',
                'sortOrdinal': 1
            }
        ]
    },
    "status": {
        "key": "status",
        "label": "Status",
        "project": None,
        "terms": [
            {
                'canonical_name': 'new',
                'key': 'new',
                'label': 'New',
                'namespace': 'new',
                'color': '#00ff00'
            },
            {
                'canonical_name': 'onhold',
                'key': 'onhold',
                'label': 'On Hold',
                'namespace': 'onhold',
                'color': '#ff9900'
            },
            {
                'canonical_name': 'resolved',
                'key': 'resolved',
                'label': 'Resolved',
                'namespace': 'resolved',
                'color': '#0c343d'
            },
            {
                'canonical_name': 'wontfix',
                'key': 'wontfix',
                'label': 'Wont Fix',
                'namespace': 'wontfix',
                'color': '#38761d'
            }
        ]
    }
}

esgvoc_mapper = {
    "cmip6": ["institution_id", "experiment_id", "source_id", "variable_id"],
    "cmip7": ["institution", "experiment", "source", "variable"],
    "cordex-cmip5": ["institute", "experiment", "rcm_model", "variable"],
    "cordex-cmip6": ["institution_id", "driving_experiment_id", 'source_id', "variable_id"],
    "input4mips": ["target_mip", "institution_id", "source_id", "variable_id"]
}

collection_mapper = {
    "cmip6": {
        "institution_id": "Organization",
        "experiment_id": "Experiment",
        "source_id": "Source",
        "variable_id": "Variable"
    },
    "cmip7": {
        "institution": "Organization",
        "experiment": "Experiment",
        "source": "Source",
        "variable": "Variable"
    },
    "cordex-cmip5": {
        "institute": "Organization",
        "experiment": "Experiment",
        "rcm_model": "Source",
        "variable": "Variable"
    },
    "cordex-cmip6": {
        "institution_id": "Organization",
        "driving_experiment_id": "Experiment",
        "source_id": "Source",
        "variable_id": "Variable"
    },
    "input4mips": {
        "target_mip": "Target MIP",
        "institution_id": "Organization",
        "source_id": "Source",
        "variable_id": "Variable"
    },
}
