import re
import logging
from typing import List, Set
from datetime import date, datetime
from collections import defaultdict

from starlette.requests import Request
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session, load_only
from sqlalchemy.orm.query import Query
from sqlalchemy.exc import AmbiguousForeignKeysError, InvalidRequestError
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import desc, or_, and_, any_, inspect, text
from sqlalchemy.util import to_list
from sqlalchemy.sql import operators, extract
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.dialects.postgresql import ARRAY

from app.db.base_class import Base

from app.crud.SearchFilter.utils import (
    get_query_as_string, 
    get_class_by_tablename
)
# from app.crud.SearchFilter.filter import FilterBase

logger = logging.getLogger(__name__)


class ParsedQueryParam(object):

    def __init__(self, field, condition, value, table_name, sa_model, sa_model_column, sa_operator, force_and=False):
        self.column = field
        self.condition = condition
        self.value = value
        self.force_and = force_and
        self.table_name = table_name
        self.sa_model = sa_model
        self.sa_model_column = sa_model_column
        self.sa_operator = sa_operator
        self.value_has_null = isinstance(self.value, list) and None in self.value[0]

        if self.condition == 'iexact':
            # iexact is used in free text search, we append % to make it case insensitive wild card search
            self.value = "%{}%".format(value)

        if self.condition == 'as':
            # as is used to skip the preprocess(converting str to int) of value which is in str(int) type
            # it helps to query the varchar type columns while having numbers as string
            self.value = "{}".format(value)

    def __hash__(self):
        return hash(self.column)

    def __eq__(self, other):
        return isinstance(other, ParsedQueryParam) and self.__dict__ == other.__dict__

    def get_sa_query_criteria(self):
        if self.value_has_null and self.condition in ['in', 'notin']:
            # if the value has null, use IS NULL and generate OR statments in (SQL) instead of using IN operator,
            # since IN (NULL) is not a valid sql clause
            sub_criteria = []
            for val in self.value[0]:
                sub_criteria.append(operators.eq(self.sa_model_column, val))
            criteria_or_ = or_(*sub_criteria)
            return criteria_or_
        else:
            # logger.debug("Framing *to_list:{}".format(to_list(self.value)))
            operator = self.sa_operator(self.sa_model_column, *to_list(self.value))
            return operator


class DbModelSearchFilter(object):
    _underscore_operators = {
        'gt': operators.gt,
        'lt': operators.lt,
        'gte': operators.ge,
        'lte': operators.le,
        'notin': operators.notin_op,
        'any': any_,
        'contains': operators.contains_op, # column @> '{value}'
        'in': operators.in_op,
        'as': operators.eq,
        'exact': operators.eq,
        'iexact': operators.ilike_op,
        'startswith': operators.startswith_op,
        'istartswith': lambda c, x: c.ilike(x.replace('%', '%%') + '%'),
        'iendswith': lambda c, x: c.ilike('%' + x.replace('%', '%%')),
        'endswith': operators.endswith_op,
        'isnull': lambda c, x: c==None if x else c!=None,
        'range': operators.between_op,
        'year': lambda c, x: extract('year', c) == x,
        'month': lambda c, x: extract('month', c) == x,
        'day': lambda c, x: extract('day', c) == x,
        'regex': lambda column, expr: column.op('~')(f'{expr}'),
        'overlap': ARRAY.Comparator.overlap # column && '{value}'
    }

    def __init__(self,
                 request: Request,
                 db_session: Session,
                 db_model: Base,
                 join_db_models: List[Base] = [],
                 join_conditions: List = None,
                #  option_filter: FilterBase = None,
                 is_outer_join: bool = False,
                 allow_override_delete: bool = False,
                 include_marketplace: bool = True,
                 use_or: bool = False,
                 additional_or_filters: List = None,
                 custom_filter_criteria: List = None,
                 filter_criteria: List = None,
                 skipped_params: List = None,
                 load_defined_columns: List = None
                 ):
        self.request: Request = request
        self.db_session: Session = db_session
        self.db_model: Base = db_model
        self.join_db_models: List[Base] = join_db_models
        self.join_conditions: List = join_conditions
        # self.option_filter: FilterBase = option_filter
        self.is_outer_join: bool = is_outer_join
        self.allow_override_delete: bool = allow_override_delete
        self.include_marketplace: bool = include_marketplace
        self.use_or: bool = use_or
        self.order_by = None
        self.date_field = None
        self.from_date = date
        self.to_date = date
        self.additional_or_filters = additional_or_filters,
        self.custom_filter_criteria = custom_filter_criteria,
        self.filter_criteria = filter_criteria,
        self.skipped_params = skipped_params,
        self.load_defined_columns = load_defined_columns
        self.mapped_joinable_tables = []
        self.mapped_joinable_onclause = {} # legacy primary joinable tables

        # mapping specified models and its columns
        self.map_tables_and_columns()

        # extracting table name from query param 
        # and mapping that table's sa_model 
        # if that sa_model has relationship with any of join_db_models or db_model 
        # then make join query 
        for param in request.query_params:
                # :param: &table_name___column=value 
                table_col_splits = param.split('___', 1)
                # logger.debug("table_col_splits:{}".format(table_col_splits))
                if len(table_col_splits) == 2:
                    table, column = table_col_splits
                    if not (column in self.column_to_table_map and table in self.column_to_table_map[column]):
                        if not (table in self.table_to_columns_map and column in self.table_to_columns_map[table]):
                            mapped_sa_model = get_class_by_tablename(Base,table)
                            if mapped_sa_model:
                                # inspecting relationship from existing model
                                for model in [db_model] + join_db_models:
                                    inspector = inspect(model)
                                    if mapped_sa_model in [r.mapper.class_ for r in inspector.relationships]:
                                        if mapped_sa_model not in join_db_models:
                                            self.join_db_models.append(mapped_sa_model)
                                        # it normalizing join conditions
                                        # elif model in self.mapped_joinable_onclause:
                                        #     self.mapped_joinable_onclause[model] = self.mapped_joinable_onclause[model].union({mapped_sa_model}) 
                                        # else:        
                                        #     self.mapped_joinable_onclause[model] = {mapped_sa_model}
                            else:
                                # logger.debug("No Base Class found for specified table {}; So, not able to filter by {}".format(table, param))
                                raise HTTPException (status_code=422, detail=f"Invalid query parameter :{param}")
                        else:
                            # logger.debug("Invalid table:{} and column:{} given in the parameter:{}".format(table, column, param))
                            raise HTTPException (status_code=422, detail=f"Invalid query parameter :{param}")
        # refershing mapped models and columns
        self.map_tables_and_columns()                   
                
    def map_tables_and_columns(self):
        models_preserving_join_order = [self.db_model] + self.join_db_models
        self.tablename_samodel_map = {model.__tablename__: model for model in models_preserving_join_order}
        self.tablename_samodel_map[self.db_model.__tablename__] = self.db_model

        # creating a map of table columns
        # python 3 dicts preserve the insertion order by default
        self.inspector = inspect(self.db_session.get_bind())
        self.table_to_columns_map = {table_name: self.get_columns_and_properties(sa_model) for
                                     table_name, sa_model in self.tablename_samodel_map.items()}
        
        # create a map of column to tables
        self.column_to_table_map = defaultdict(list)
        for table in self.tablename_samodel_map:
            for col in self.table_to_columns_map[table]:
                self.column_to_table_map[col].append(table)

    def get_columns_and_properties(self, sa_model):
        columns = [col['name'] for col in self.inspector.get_columns(sa_model.__tablename__)]
        hybrid_properties = [attr.__name__ for attr in inspect(sa_model).all_orm_descriptors if
                             type(attr) == hybrid_property]
        return columns + hybrid_properties

    def parse_param_value(self, param, value):

        def fix_type(value: str):
            if value.isdigit():
                value = int(value)
            else:
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.lower() == 'null':
                    value = None
            return value

        def preprocess_value(condition: str, value: str):

            if condition in ['in', 'notin']:
                processed_value = [[fix_type(val) for val in value.split(',')]]
            elif condition == 'range':
                processed_value = [fix_type(val) for val in value.split(',')]
            else:
                processed_value = fix_type(value)
            return processed_value

        force_and: bool = False
        condition: str = 'exact'
        table: str = None
        column: str = None
        processed_value = None
        model: Base = None

        # logger.debug("Starting parsing | param:{}|".format(param))
        FORCE_AND_STR = '__and'
        if param.endswith(FORCE_AND_STR):
            force_and = True
            param = param[:-len(FORCE_AND_STR)] # remove '__and' from param

        # logger.debug("After force_and Parsing | param:{}|force_and:{}|".format(param, force_and))

        has_cond_pattern = r'(.*)__({})$'.format('|'.join(self._underscore_operators.keys()))
        has_cond_match = re.search(has_cond_pattern, param)
        if has_cond_match:
            condition = has_cond_match.group(2)
            param = has_cond_match.group(1)

        # logger.debug("After Has Condition Parsing | param:{}|force_and:{}|condition:{}|".format(param, force_and, condition))

        if '.' in param: #(join db model eg:join_db_model.column)
            ref_tbl_col =[col for col in param.split('.')]
            table = ref_tbl_col[0] # table name (Note: this table should be one of join_db_models)
            column = ref_tbl_col[1] # column name
        else:
            table_col_splits = param.split('___', 1)
            # logger.debug("table_col_splits:{}".format(table_col_splits))
            if len(table_col_splits) == 2:
                table, column = table_col_splits
                if not (column in self.column_to_table_map and table in self.column_to_table_map[column]):
                    raise ValueError(
                        "Invalid table:{} and column:{} given in the parameter:{}".format(table, column, param))
            else:
                column = table_col_splits[0]

        if table is None and column in self.column_to_table_map:
            table = self.column_to_table_map[column][0]

        if table is None or column is None:
            raise ValueError(
                "Invalid table:{} and column:{} given in the parameter:{}".format(table, column, param))

        model = self.tablename_samodel_map[table]
        model_column = getattr(model, column)
        op = self._underscore_operators[condition]
        if isinstance(value,list):
            processed_value = [value]
        else:
            processed_value = preprocess_value(condition, value)

        if processed_value is None or column is None:
            raise ValueError(
                "Invalid column:{} | value:{}".format(column,value))
        logger.debug(
            "After Table Column parsing | param:{}|force_and:{}|condition:{}|table:{}|column:{}|value:{}|processed_value:{}|".format(
                param,
                force_and,
                condition,
                table,
                column,
                value,
                processed_value))

        return ParsedQueryParam(field=column, condition=condition, value=processed_value, force_and=force_and,
                                table_name=table, sa_model=model, sa_model_column=model_column, sa_operator=op)

    def get_filtered_data(self, all_rows=False, fetch_row_count=False):

        self.set_query_options()
        self.query_params = self.get_query_params()
        # logger.debug(f'query_params are: {self.query_params}')
        query = self.get_sa_query()

        # apply filters from base model
        query = self.apply_query_params(query, self.query_params)

        # apply quick search params
        if 'searchTerm' in self.request.query_params:
            query = self.apply_quick_search_query_params(query, self.request.query_params['searchTerm'])
        
        #+++++++++++++++++++disabled for now++++++++++++++++
        # query = self.apply_optional_filters(query)
        #+++++++++++++++++++disabled for now++++++++++++++++

        if self.filter_criteria:
            query = self.apply_filters(query)

        # apply custom_filter_criteria
        if self.custom_filter_criteria:
            query = self.apply_custom_filter_criteria(query)

        # apply additional_or_filters, if present
        if self.additional_or_filters:
            query = self.apply_additional_or_query_params(query)

        # set self.allow_override_delete to True if you want to query deleted rows
        if not self.allow_override_delete:
            query = add_delete_filter(query, self.db_model)
            for model in self.join_db_models:
                query = add_delete_filter(query, model, True)

        # apply date_range filter, if present
        query = self.add_date_range_filter(query)

        # set distinct on all primary keys of the main table, so we get unique main table objects in the query result
        query = add_distinct_filter(query, self.db_model)

        query = self.apply_order_by(query)

        query = self.apply_pagination(all_rows, query)

        logger.info(
            "SQL query for the query string:{}".format(self.request.scope.get("query_string", '').decode('utf-8')))
        logger.info(get_query_as_string(query))

        if fetch_row_count:
            return query.count()
        else:
            return query.all()

    def apply_pagination(self, all_rows, query):
        if not all_rows:
            skip = int(self.request.query_params.get('skip', 0))
            query = query.offset(skip)
            limit = int(self.request.query_params.get('limit', 10))
            query = query.limit(limit)
            logger.info("the limit is {},skip is {}, all_rows is {}".format(limit, skip, all_rows))
        return query

    def apply_order_by(self, query):
        # the order by columns should also included in the distinct to frame a valid sql
        # https://stackoverflow.com/questions/9795660/postgresql-distinct-on-with-different-order-by
        if self.order_by:
            attrs = self.order_by.split(',')
            logger.info(attrs)
            for attr in attrs:
                descending = False
                if attr[0] in '+-':
                    if attr[0] == '-':
                        descending = True
                    attr = attr[1:]
                try:
                    if attr.startswith('coalesce'):
                        attrs = attr.split('__')
                        column_1 = getattr(self.db_model, attrs[1])
                        column_2 = getattr(self.db_model, attrs[2])
                        query.distinct(coalesce(column_1, column_2))
                        if descending:
                            query = query.order_by(desc(coalesce(column_1, column_2)))
                        else:
                            query = query.order_by(coalesce(column_1, column_2))
                    else:
                        column = getattr(self.db_model, attr)
                        query.distinct(column)
                        if descending:
                            query = query.order_by(desc(column))
                        else:
                            query = query.order_by(column)
                except AttributeError:
                    logger.warning('missing attr, not including in order by:{}'.format(attr))
                    pass
        return query

    def get_sa_query(self):
        query = self.db_session.query(self.db_model)
            
        def apply_manual_onclause_joins(query,join_conditions_:List,join_db_models_:List):
            for model,condition in zip(join_db_models_,join_conditions_):
                try:
                    query = query.join(model,condition,isouter=self.is_outer_join)
                except Exception as e:
                    # logger.debug(query)
                    logger.debug(e) 
            return query

        # join models
        if self.join_db_models is not None and self.join_db_models:
            print(self.join_db_models)
            try:
                # to reduce join 
                # for model in self.join_db_models:
                #     if self.mapped_joinable_onclause:
                #             if model in self.mapped_joinable_onclause:
                #                 for mapped_model in self.mapped_joinable_onclause[model]:
                #                     query = query.join(model,mapped_model,isouter=self.is_outer_join)
                #     else:
                query = query.join(*self.join_db_models, isouter=self.is_outer_join)
            except AmbiguousForeignKeysError as afe:
                if not self.join_conditions:
                    logger.debug(afe)
                    logger.debug("NOTE : use the list of manual 'join_conditions' param like [left.column == right.column,...]")
                else:
                    query = apply_manual_onclause_joins(query,self.join_conditions,self.join_db_models)      
            except InvalidRequestError as e:
                if self.join_conditions:
                    try:
                        query = apply_manual_onclause_joins(query,self.join_conditions,self.join_db_models)
                    except Exception as e:
                        logger.error(e)
                        logger.debug("not able to generate join based on specified creteria in join_conditions")
                else:
                    logger.error(
                        "Check the usage specified for DBModelSearchFilter.join_db_models, No foreign keys exist")
        
        raw_load_columns = []
        finalized_load_columns = []
        if not self.load_defined_columns is None:
            for col in self.load_defined_columns:
                if isinstance(col, str):
                    try:
                        finalized_load_columns.append(getattr(self.db_model, col))
                    except AttributeError as e:
                        logger.error(e)
                        logger.debug(f"{col} is not a valid column name which is specified in load_defined_columns")
                else:
                    raw_load_columns.append(col)
            if finalized_load_columns:
                query = query.options(load_only(*finalized_load_columns))
            elif raw_load_columns:
                query = query.with_entities(*raw_load_columns)
                        
        return query

    def apply_optional_filters(self, query: Query) -> Query:
        if self.option_filter is not None:
            field_filters = self.option_filter.dict(exclude_unset=True)
            for field in field_filters.keys():
                if field in self.column_to_table_map:
                    table = self.column_to_table_map[field][0]
                    sa_model = self.tablename_samodel_map[table]
                    column = getattr(sa_model, field)
                    in_operator = self._underscore_operators['in']
                    if field_filters[field] is not None:
                        optional_filter_values = [field_filters[field]]
                        # logger.debug("optional filter values:{}".format(optional_filter_values))
                        query = query.filter(in_operator(column, optional_filter_values))
        return query

    def apply_query_params(self, query: Query, parsed_params: Set[ParsedQueryParam]) -> Query:
        filter_criterian = []
        force_and_criterian = []
        for param in parsed_params:
            sa_query_criteria = param.get_sa_query_criteria()
            # logger.info(param)
            # logger.info(sa_query_criteria)
            if param.force_and:
                force_and_criterian.append(sa_query_criteria)
            else:
                filter_criterian.append(sa_query_criteria)
        if self.use_or:
            query = query.filter(or_(*filter_criterian))
        else:
            query = query.filter(*filter_criterian)

        if force_and_criterian:
            query = query.filter(and_(*force_and_criterian))

        return query

    def apply_quick_search_query_params(self, query: Query, value: str) -> Query:
        """apply quick search (full text search) params if any
        # if query_param is searchTerm, then there is full text search also
        # so get the columns marked for quick search in the model
        # and use them as individual parameters with iexact
        """
        # logger.debug('inside apply_quick_search_query_params')
        invalid_params = []
        # logger.debug(f'searchTerm value is: {value}')
        # logger.debug(f'db_model name is: {self.db_model.__name__}')
        try:
            if self.db_model.quick_search_columns:
                # logger.debug(f'quick_search_columns are: {self.db_model.quick_search_columns}')
                quick_search_filter_criteria = []
                for column in self.db_model.quick_search_columns:
                    if value.isdigit():
                        if column == 'id' or column.endswith('_id'):  # int columns
                            query_param = column  # apply == operator
                        elif column == 'uid' or column.endswith('_uid'):  # int columns
                            query_param = column  # apply == operator
                        else:
                            continue  # just skip the non int columns
                    else:
                        if column == 'id' or column.endswith('_id'):
                            continue  # just skip the int columns
                        elif column == 'uid' or column.endswith('_uid'):  # int columns
                            continue  # just skip the int columns
                        else:
                            query_param = column + '__iexact'

                    try:
                        parsed_param = self.parse_param_value(query_param, value)
                        sa_query_criterian = parsed_param.get_sa_query_criteria()
                        quick_search_filter_criteria.append(sa_query_criterian)
                    except ValueError as e:
                        logger.debug(str(e))
                        logger.debug("Ignoring invalid parameter:{}={}".format(query_param, value))
                        invalid_params.append((query_param, value))
                # form a condition with OR for all these columns
                qfc = or_(*quick_search_filter_criteria)
                # logger.debug(f'quick search filter criteria is: {qfc}')
                query = query.filter(qfc)
        except AttributeError as ae:
            logger.debug('skipping apply_quick_search_query_params..')
            logger.info(ae)

        return query

    def apply_additional_or_query_params(self, query: Query) -> Query:
        """apply additional or query params"""
        additional_or_filter_list = None
        if isinstance(self.additional_or_filters, tuple):
            additional_or_filter_list = self.additional_or_filters[0]
        else:
            additional_or_filter_list = self.additional_or_filters

        additional_or_filter_criteria = []
        if additional_or_filter_list:
            # logger.debug('inside apply_additional_or_query_params')
            invalid_params = []
            # logger.debug(f'additional_or_filters is: {self.additional_or_filters}')
            for additional_or_filter in additional_or_filter_list:
                for query_param in additional_or_filter:
                    value = additional_or_filter[query_param]
                    # logger.debug(f'additional or query param is: {query_param}')
                    # logger.debug(f'additional or query param value is: {value}')
                    try:
                        parsed_param = self.parse_param_value(query_param, value)
                        sa_query_criterian = parsed_param.get_sa_query_criteria()
                        additional_or_filter_criteria.append(sa_query_criterian)
                    except ValueError as e:
                        logger.debug(str(e))
                        logger.debug("Ignoring invalid parameter:{}={}".format(query_param, value))
                        invalid_params.append((query_param, value))
                # form a condition with OR for all these columns
                qfc = or_(*additional_or_filter_criteria)
                # logger.debug(f'additional or filter criteria is: {qfc}')
                query = query.filter(qfc)

        return query

    def apply_filters(self,query:Query)->Query:
        " apply_custom_filters "
        filter_criteria_list = None
        if isinstance(self.filter_criteria,tuple):
            filter_criteria_list = self.filter_criteria[0] 
        else:
            filter_criteria_list = self.filter_criteria
        
        if filter_criteria_list:
            for criteria in filter_criteria_list:
                query = query.filter(criteria)
            
        return query

    def apply_custom_filter_criteria(self,query:Query)->Query:
        """ apply custom filter criteria """
        custom_filter_criteria_list = None
        if isinstance(self.custom_filter_criteria,tuple):
            custom_filter_criteria_list = self.custom_filter_criteria[0] 
        else:
            custom_filter_criteria_list = self.custom_filter_criteria
        def parse_sa_condition(condition_key):
            condition = and_
            if condition_key.startswith("or"):
                condition = or_

            return condition

        column_level_condition = None
        criteria_level_condition = None
        if custom_filter_criteria_list:
            # logger.debug('processing apply_custom_filter_criteria')
            invalid_params = []
            # logger.debug(f'custom_filter_criteria is: {self.custom_filter_criteria}')
            for items in range(len(custom_filter_criteria_list)):
                # logger.debug(f"items_:{items}") # 0
                for item in custom_filter_criteria_list[items]:
                    custom_filter_criteria = []
                    criteria_level_condition = parse_sa_condition(item)
                    item = custom_filter_criteria_list[items][item]
                    # logger.debug(f"item_:{item}")
                    for child_item in item:
                        # logger.debug(f"child_item_:{child_item}")
                        sub_custom_filter_criteria = []
                        column_level_condition = parse_sa_condition(child_item)
                        for query_param in item[child_item].keys():
                            value = item[child_item][query_param]
                            # logger.debug(f"query_param: {query_param} | value: {value}")
                            try:
                                parsed_param = self.parse_param_value(query_param, value)
                                sa_query_criterian = parsed_param.get_sa_query_criteria()
                                sub_custom_filter_criteria.append(sa_query_criterian)
                            except Exception as ex:
                                logger.info(f"invalid colum :{query_param} | value: {value} in custom_filter_criteria")
                                invalid_params.append(query_param)
                        # form a specified condition for all these columns
                        logger.debug(f"invalid params: {invalid_params}")
                        # logger.debug(f"column_level_condition:{column_level_condition}")
                        # logger.debug(f'sub_custom_filter_criteria{column_level_condition(*sub_custom_filter_criteria)}')
                        qfc_1 = column_level_condition(*sub_custom_filter_criteria)
                        # logger.debug(f"child_qfc: {qfc_1}")
                        custom_filter_criteria.append(qfc_1)
                    # commonly form a condition with AND for all these filter criteria
                    # logger.debug(f"criteria_level_condition:{criteria_level_condition}")
                    qfc_0 = criteria_level_condition(*custom_filter_criteria)
                    # logger.debug(f"parent_qfc: {qfc_0}")
                    # logger.debug(f'custom filter criteria is: {qfc_0}')
                    query = query.filter(qfc_0)
        return query
        


    def add_date_range_filter(self,query):
        date_1=self.request.query_params.get('from_date')
        date_2=self.request.query_params.get('to_date')
        dot = '.'
        column = None
        if self.date_field:
            logger.info("the date_field is {}".format(self.date_field))
            if dot not in self.date_field:
                try:
                    column = getattr(self.db_model, self.date_field)
                    # query = query.filter(column.between(date_1+'T00:00:01', date_2+'T23:59:59'))
                except AttributeError:
                    logger.warning('missing attr, unknown column:{}'.format(self.date_field))
                    pass
            elif dot in self.date_field:
                try:
                    tbl_column = self.date_field.split(dot)
                    # logger.debug(f'mapped_list :{tbl_column}')
                    for table_name in self.inspector.get_table_names(schema='public'):
                        if table_name == tbl_column[0]:
                            mapped_sa_model = [obj for obj in self.join_db_models if obj.__tablename__ == table_name][0]
                            current_time = '{time:%H:%M:%S}'.format(time=datetime.now())
                            for column_ in self.inspector.get_columns(table_name):
                                if column_['name'] == tbl_column[1]:
                                    mapped_column = getattr(mapped_sa_model, column_['name'])
                                    # logger.debug("mapped column_name: %s" % mapped_column)
                                    column = mapped_column
                                    # query = query.filter(mapped_column.between(date_1+'T'+current_time,date_2+'T'+current_time))
                except Exception as e:
                    logger.debug(f"date_filter_skipped; can't map the column you specified as date_field: {self.date_field}")
                    logger.info(e)
            if column is not None and (date_1 or date_2):
                if date_1 and date_2:
                    logger.info(f"start_date is {date_1}, end_date is {date_2}")
                    query = query.filter(column.between(date_1+'T00:00:00', date_2+'T23:59:59'))
                elif date_1: # from_date
                    logger.info(f"start_date is {date_1}")
                    query = query.filter(column >= date_1+'T00:00:00')
                elif date_2: # to_date
                    logger.info(f"end_date is {date_2}")
                    query = query.filter(column <= date_2+'T23:59:59')
            # logger.debug("date_filter_skipped !!!")


        return query

    def set_query_options(self):
        self.order_by = self.request.query_params.get('order_by')
        self.date_field = self.request.query_params.get('date_field')
        for query_param in self.request.query_params:
            value = self.request.query_params[query_param]
            if query_param == 'use_or' and value == 'true':
                self.use_or = True
            elif query_param == 'include_marketplace' and value == 'true':
                self.include_marketplace = True

    def get_query_params(self) -> Set[ParsedQueryParam]:
        parsed_params = set()
        invalid_params = []
        skipped_query_params = [
            'use_or', 
            'order_by', 
            'include_marketplace', 
            'skip', 
            'offset', 
            'limit', 
            'from_date', 
            'to_date', 
            'date_field', 
            'all_rows'
            ]
        for query_param in self.request.query_params:
            value = self.request.query_params[query_param]
            if self.skipped_params:
                if isinstance(self.skipped_params,tuple) and self.skipped_params[0] is not None:
                    skipped_query_params.extend(self.skipped_params[0])
                else:
                    skipped_query_params.extend(self.skipped_params)
            
            # logger.debug('____'*10)
            # logger.debug(f'skipping query params : {skipped_query_params}')
            # logger.debug('____'*10)

            if query_param in skipped_query_params:
                continue
            else:
                try:
                    parsed_param = self.parse_param_value(query_param, value)
                    parsed_params.add(parsed_param)
                except ValueError as e:
                    logger.debug(str(e))
                    logger.debug("Ignoring invalid parameter:{}={}".format(query_param, value))
                    invalid_params.append((query_param, value))
        return parsed_params


def add_distinct_filter(query: Query, model: Base) -> Query:
    inspect_model = inspect(model)
    fields = [field.key for field in inspect_model.primary_key]
    for field in fields:
        try:
            column = getattr(model, field)
            query = query.distinct(column)
        except AttributeError:
            pass
    return query


def add_delete_filter(query: Query, model: Base, is_nullable=False) -> Query:
    try:
        column = getattr(model, 'deleted')
        if is_nullable:
            query = query.filter(or_(column == False, column == None))
        else:
            query = query.filter(column == False)
    except AttributeError:
        pass
    return query
