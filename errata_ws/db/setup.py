from sqlalchemy.schema import CreateSchema

from errata_ws.db import session as db_session
from errata_ws.db.utils import METADATA



# Set of db schemas.
_SCHEMAS = {'errata'}


def execute():
    """
    Sets up a database.
    """

    # Initialize schemas.
    with db_session.sa_engine.begin() as conn:
        for schema in _SCHEMAS:
            conn.execute(CreateSchema(schema, if_not_exists=True))

    # Initialize tables.
    METADATA.create_all(db_session.sa_engine)
