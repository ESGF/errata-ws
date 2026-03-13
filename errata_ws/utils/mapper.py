import esgvoc.api as ev
from resources.esdoc_map import esdoc_map


def map_collection(identifier):
    """Converts a esgvoc collection and its terms to a dictionary.

    """
    authority, project, collection = identifier.split(":")

    if authority == "wcrp":
        result = {
            'canonical_name': collection,
            'key': f"{authority}:{project}:{collection}",
            'label': collection,
            'namespace': f"{authority}:{project}:{collection}",
            'terms': [map_term(term, project, collection) for term in ev.get_all_terms_in_collection(project, collection) if authority == "wcrp"]
        }
    elif authority == "esdoc":
        result = esdoc_map[identifier]

    return result


def map_term(term, project, collection):
    """Converts a esgvoc term to a dictionary.

    """
    result = {
        'canonical_name': term.id,
        'key': f"wcrp:{project}:{collection}:{term.id}",
        'label': term.drs_name if hasattr(term, "drs_name") else term.id,
        'namespace': f"wcrp:{project}:{collection}:{term.id}"
    }
    result.update(term.model_dump(mode="json"))

    return result