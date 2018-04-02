from a_tuin.unittests.api.fixtures.models import areferringclass__aclass

__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import graphene

from graphene import Node
from graphql_relay.connection.arrayconnection import cursor_to_offset, offset_to_cursor
from unittest.mock import Mock

from a_tuin.api.connection import node_connection_field

from a_tuin.unittests.api.graphql_schema_test_case import GraphQLSchemaTestCase
from a_tuin.unittests.api.fixtures.mapping import AClass, AClassQuery, AReferringClass, AReferringClassQuery
from a_tuin.unittests.api.fixtures.nodes import AClassNode, AReferringClassNode

aclass_connection_field = node_connection_field(
    AClass,
    AClassQuery,
    AClassNode,
    description="Fixture class"
)

areferring_connection_field = node_connection_field(
    AReferringClass,
    AReferringClassQuery,
    AReferringClassNode,
    description="Fixture referring class"
)

class RootQueryType(graphene.ObjectType):
    node = Node.Field()
    aclasses = aclass_connection_field
    areferringclasses = areferring_connection_field


schema = graphene.Schema(query=RootQueryType)


class TestConnection(GraphQLSchemaTestCase):

    def test_connection_field(self):

        root_tested = False
        filter_tested = False
        connection_tested = False
        edge_tested = False
        aclass_tested = False

        for reported_type in self.get_types(schema):
            if reported_type['name'] == 'RootQueryType':
                self.assertEqual(
                    (
                        ('filters', 'AClassNodeFilterInput'),
                        ('orderBy', 'String'),
                        ('before', 'String'),
                        ('after', 'String'),
                        ('first', 'Int'),
                        ('last', 'Int'),
                    ),
                    tuple(
                        (arg['name'], arg['type']['name'])
                        for arg in reported_type['fields'][0]['args']
                    )
                )
                root_tested = True
            if reported_type['name'] == 'AClassNodeFilterInput':
                self.assertEqual(
                    (
                        ('refNo', 'Int'),
                        ('name', 'String'),
                        ('isRunning', 'Boolean'),
                        ('status', 'AClassStatus'),
                        ('date', 'DateTime'),
                    ),
                    tuple(
                        (arg['name'], arg['type']['name'])
                        for arg in reported_type['inputFields']
                    )
                )
                filter_tested = True
            if reported_type['name'] == 'AClassNodeConnection':
                self.assertEqual(
                    ('pageInfo', 'edges', 'totalCount', 'filteredCount'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                self.assertEqual(
                    'AClassNodeEdge',
                    reported_type['fields'][1]['type']['ofType']['ofType']['name']
                )
                connection_tested = True
            if reported_type['name'] == 'AClassNodeEdge':
                self.assertEqual(
                    'AClassNode',
                    reported_type['fields'][0]['type']['name']
                )
                edge_tested = True
            if reported_type['name'] == 'AClassNode':
                self.assertEqual(
                    ('id', 'refNo', 'name', 'isRunning', 'status', 'date', 'refers'),
                    tuple(field['name'] for field in reported_type['fields'])
                )
                aclass_tested = True

        self.assertTrue(root_tested)
        self.assertTrue(filter_tested)
        self.assertTrue(connection_tested)
        self.assertTrue(edge_tested)
        self.assertTrue(aclass_tested)

    class InfoFixture(object):
        def __init__(self, context):
            self.context = context

    def _apply_filter_with_mocks(self, num_instances, offset, limit, filters, order_by):
        expected_instances = [Mock() for _ in range(num_instances)]
        # mock entities with row numbers
        mock_results = [(instance, index + 1) for index, instance in enumerate(expected_instances)]
        mock_query = Mock()
        mock_session = Mock()
        mock_query.add_columns.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = len(mock_results)

        def apply_offset():
            del mock_results[0:offset]
            del expected_instances[0:offset]
            return mock_query

        mock_query.from_self.side_effect = apply_offset

        def apply_limit(num_results):
            del mock_results[num_results:]
            del expected_instances[num_results:]
            return mock_query

        mock_query.limit.side_effect = apply_limit
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_results
        mock_session.query.return_value = mock_query

        context = {'request': {'session': mock_session}}
        args = {}
        if offset:
            args['after'] = offset_to_cursor(offset)
        if limit:
            args['first'] = limit
        if filters:
            args['filters'] = filters
        if order_by:
            args['orderBy'] = order_by

        info = TestConnection.InfoFixture(context)

        instances = aclass_connection_field.resolver(
            None, info, **args
        )

        return context, expected_instances, instances, mock_query, mock_session

    def _assert_standard_checks(self, expected_instances, instances, mock_session, mock_query):
        self.assertEqual(expected_instances, instances)
        mock_session.query.assert_called_with(AClass)
        self.assertEqual(2, mock_session.query.call_count)
        mock_query.count.assert_called_once_with()
        mock_query.all.assert_called_once_with()

    def _assert_offset(self, offset, mock_query):
        offset_expression = mock_query.filter.call_args_list[2][0][0]
        self.assertEqual('_row_number', offset_expression.left.key)
        self.assertEqual(offset, offset_expression.right.value - 1)
        mock_query.from_self.assert_called_once_with()

    def _assert_filter(self, filters, mock_query):
        filter_expressions = {
            expression.left.description: expression.right.value
            for criterion in mock_query.filter.call_args_list[0]
            for expression in criterion
        }
        self.assertEqual(filters, filter_expressions)

    def _assert_page_info(self, page_info, has_next, has_prev, start, end):
        self.assertEqual(has_next, page_info.has_next_page)
        self.assertEqual(has_prev, page_info.has_previous_page)
        self.assertEqual(start, cursor_to_offset(page_info.start_cursor))
        self.assertEqual(end, cursor_to_offset(page_info.end_cursor))

    def test_resolve_filter_no_page(self):
        num_instances = 14
        limit = None
        offset = None
        filters = {'status': 1, 'name': 'somename'}

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, offset, limit, filters, None
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        self.assertEqual(num_instances, context['count'])
        self._assert_filter(filters, mock_query)
        self._assert_page_info(context['pageInfo'], False, False, 0, num_instances - 1)

    def test_resolve_filter_first_page(self):
        num_instances = 9
        limit = 4
        offset = 0
        filters = {'status': 1}

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, offset, limit, filters, None
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        self.assertEqual(limit, context['count'])
        self._assert_filter(filters, mock_query)
        mock_query.limit.assert_called_once_with(limit)
        self._assert_page_info(context['pageInfo'], True, False, 0, limit - 1)

    def test_resolve_filter_middle_page(self):
        num_instances = 22
        limit = 4
        offset = 13
        filters = {'status': 1, 'name': 'somename'}

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, offset, limit, filters, None
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        self.assertEqual(limit, context['count'])
        self._assert_offset(offset, mock_query)
        self._assert_filter(filters, mock_query)
        mock_query.limit.assert_called_once_with(limit)
        self._assert_page_info(context['pageInfo'], True, True, offset, offset + limit - 1)

    def test_resolve_filter_last_page(self):
        num_instances = 17
        limit = 6
        offset = 14
        filters = {'name': 'somename'}

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, offset, limit, filters, None
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        self.assertEqual(num_instances - offset, context['count'])
        self._assert_offset(offset, mock_query)
        self._assert_filter(filters, mock_query)
        mock_query.limit.assert_called_once_with(limit)
        self._assert_page_info(context['pageInfo'], False, True, offset, num_instances - 1)

    def test_sort_one_ascending(self):
        num_instances = 12
        order_by = 'name'

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, None, None, None, order_by
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        call_args = mock_query.order_by.call_args_list[0]
        self.assertEqual(order_by, call_args[0][0].element.name)
        self.assertIn('ASC', str(call_args[0][0].expression))

    def test_sort_one_descending(self):
        num_instances = 12
        order_by = 'refNo'
        order_by_with_direction = '-{}'.format(order_by)

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, None, None, None, order_by_with_direction
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)
        call_args = mock_query.order_by.call_args_list[0]
        self.assertEqual('ref_no', call_args[0][0].element.name)
        self.assertIn('DESC', str(call_args[0][0].expression))

    def test_sort_ascending_descending(self):
        num_instances = 9
        order_by_with_direction = 'refNo,-name'

        context, expected_instances, instances, mock_query, mock_session = self._apply_filter_with_mocks(
            num_instances, None, None, None, order_by_with_direction
        )

        self._assert_standard_checks(expected_instances, instances, mock_session, mock_query)

        sort_expression = mock_query.order_by.call_args_list[0][0][0]
        self.assertEqual('ref_no', sort_expression.element.name)
        self.assertIn('ASC', str(sort_expression.expression))

        sort_expression = mock_query.order_by.call_args_list[0][0][1]
        self.assertEqual('name', sort_expression.element.name)
        self.assertIn('DESC', str(sort_expression.expression))

    def test__filter_casts(self):
        num_instances = 4
        offset = 0
        limit = 3
        aclass_id = 6666
        aclass_global_id = Node.to_global_id('AClass', aclass_id)
        filters = {'aclass': aclass_global_id}
        order_by = None

        expected_instances = [Mock() for _ in range(num_instances)]
        # mock entities with row numbers
        mock_results = [(instance, index + 1) for index, instance in enumerate(expected_instances)]
        mock_query = Mock()
        mock_session = Mock()
        mock_query.add_columns.return_value = mock_query

        def apply_filter(criteria):
            # check that AClass id has been decoded correctly
            self.assertEqual(str(aclass_id), criteria.right.value)
            return mock_query

        mock_query.filter.side_effect = apply_filter
        mock_query.count.return_value = len(mock_results)

        def apply_offset():
            del mock_results[0:offset]
            del expected_instances[0:offset]
            return mock_query

        mock_query.from_self.side_effect = apply_offset

        def apply_limit(num_results):
            del mock_results[num_results:]
            del expected_instances[num_results:]
            return mock_query

        mock_query.limit.side_effect = apply_limit
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = mock_results
        mock_session.query.return_value = mock_query

        context = {'request': {'session': mock_session}}
        args = {}
        if offset:
            args['after'] = offset_to_cursor(offset)
        if limit:
            args['first'] = limit
        if filters:
            args['filters'] = filters
        if order_by:
            args['orderBy'] = order_by

        info = TestConnection.InfoFixture(context)

        instances = areferring_connection_field.resolver(
            None, info, **args
        )
