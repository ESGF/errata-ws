import random
import datetime
import uuid

import esgvoc.api as ev
from esgvoc.api.project_specs import DrsType
from esgvoc.apps.drs.generator import DrsGenerator

from errata_ws.utils.constants import *

from resources.mappers import metadata_mapper


# Global now.
_NOW = datetime.datetime.now(datetime.timezone.utc)

# Collection of materials, i.e. supporting images, graphs ... etc.
_MATERIALS = []


def create_issue_dict():
    """Returns a test issue (dictionary encoding).

    """
    projects = ev.get_all_projects()
    project = random.choice(projects)

    return {
        JF_DATASETS: get_dataset_ids(project),
        JF_DESCRIPTION: str(uuid.uuid4()),
        JF_MATERIALS: get_materials(),
        JF_PROJECT: project,
        JF_SEVERITY: random.choice(metadata_mapper["severity"]["terms"])["canonical_name"],
        JF_STATUS: ISSUE_STATUS_NEW,
        JF_TITLE: str(uuid.uuid4()),
        JF_UID: str(uuid.uuid4()),
        JF_URLS: ['https://www.google.com/']
    }


def get_materials():
    """Returns test affected  datasets.

    """
    return [
        'https://www.ornithomedia.com/wp-content/uploads/2025/12/news031225-kakapo.jpg',
        'https://rodmaps.com/wp-content/uploads/2024/10/Sejour-de-peche-grosse-truite-en-Espagne.jpg',
        'https://live.staticflickr.com/5027/5568162083_02ec8a29f6_b.jpg',
        'https://anasazivet.com/wp-content/uploads/2019/09/pets-4415649_1920.jpg'
    ]


def get_dataset_ids(project, existing=[]):
    """Returns a collection of test dataset identifiers.

    :param str project: Project code.
    :param list existing: Dataset identifiers to be included in the result.

    :returns: Collection of test datasets.
    :rtype: list

    """
    return [get_dataset_id(project) for i in range(5)] + existing


def get_dataset_id(project):
    """Returns a dataset identifier.

    """
    generator = DrsGenerator(project_id=project)
    drs_mapping = {}
    project_specs = ev.get_project(project)

    if project_specs:
        drs_specs = project_specs.drs_specs
        if drs_specs:
            for part in drs_specs[DrsType.DATASET_ID].parts:
                collection = part.source_collection
                if collection in ["member_id", "variant_label", "driving_variant_label"]:
                    drs_mapping[collection] = "r1i1p1f1"
                elif collection == "version_realization":
                    if project == "cordex-cmip6":
                        drs_mapping[collection] = "v1-r1"
                    else:
                        drs_mapping[collection] = "v1"
                elif collection == "branding_suffix":
                    drs_mapping[collection] = random.choice(ev.get_all_terms_in_collection(project, "branded_variable")).branding_suffix_name
                elif collection in ["directory_date", "version"]:
                    drs_mapping[collection] = "v20230512"
                else:
                    random_term = random.choice(ev.get_all_terms_in_collection(project, collection))
                    drs_mapping[collection] = random_term.drs_name
    
    return f"{generator.generate_dataset_id_from_mapping(mapping=drs_mapping).generated_drs_expression}#20190704"
