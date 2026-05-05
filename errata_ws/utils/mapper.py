import esgvoc.api as ev

from resources.mappers import collection_mapper


def map_collection(project, collection):
    """
    Converts a esgvoc collection and its terms to a dictionary.
    """
    result = {
        "key": collection,
        "label": collection_mapper[project][collection],
        "project": project,
        "terms": [map_term(term, project, collection) for term in ev.get_all_terms_in_collection(project, collection)]
    }

    return result


def map_term(term, project: str, collection: str):
    """
    Converts a esgvoc term to a dictionary.
    """

    result = {
        "key": term.id,
        "label": term.drs_name if hasattr(term, "drs_name") else term.id,
        "project": project,
        "collection": collection
    }
    result.update(term.model_dump(mode="json"))

    return result