# Import all the db_models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
# from app.db_models.item import Item  # noqa
# from app.db_models.user import User  # noqa


# Import all the models, so that Base has them before being
# imported by Alembic
from collections import OrderedDict
from pkgutil import walk_packages
from importlib import import_module
from inspect import isclass
import sys
from traceback import print_tb
from app.db.base_class import Base  # noqa
import sqlalchemy as sa
import logging


from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty

logger = logging.getLogger(__name__)


def import_sa_models():
    def onerror(name):
        logger.debug('=' * 100)
        logger.debug("Error importing module %s" % name)
        type, value, traceback = sys.exc_info()
        print_tb(traceback)
        logger.debug('=' * 100)

    import app.db_models
    modules = walk_packages(path=app.db_models.__path__, prefix='app.db_models.', onerror=onerror)
    for (_, module_name, _) in modules:
        # import the module and iterate through its attributes
        module = import_module(module_name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute):
                # Add the class to this package's variables
                # logger.debug("Importing {}.{}".format(module_name, attribute_name))
                globals()[attribute_name] = attribute
