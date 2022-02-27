from sqlalchemy.dialects import postgresql, __all__


def get_query_as_string(query):
    query_string = query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    return query_string

def get_class_by_tablename(Base, tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c