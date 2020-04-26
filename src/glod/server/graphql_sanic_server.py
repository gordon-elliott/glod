__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging
import pkg_resources

from sanic import Sanic
from sanic.response import text, json
from sanic.exceptions import RequestTimeout, ServerError
from sanic_jinja2 import SanicJinja2, PackageLoader
from graphql.execution.executors.asyncio import AsyncioExecutor

from a_tuin.constants import SESSION, EXCEPTIONS_TRAPPED
from glod.configuration import configuration
from glod.db.engine import Session      # it is important to import from glod.db.engine in order that the session is bound to a db engine
from glod.api.schema import schema
from glod.server.graphql_compatibility_wrapper import GraphQLCompatibilityWrapper


LOG = logging.getLogger(__file__)
app = Sanic(__name__)
jinja = SanicJinja2(app, PackageLoader('glod', 'crudl/templates'))


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    request[SESSION] = Session()


@app.middleware('response')
async def commit_session(request, response):
    if request.get(EXCEPTIONS_TRAPPED):
        raise ServerError(request[EXCEPTIONS_TRAPPED])

    # after each request commit and close the session
    request[SESSION].commit()
    request[SESSION].close()


@app.exception(ServerError)
def rollback_session(request, exception):

    request[SESSION].rollback()
    request[SESSION].close()

    trapped_exceptions = request.get(EXCEPTIONS_TRAPPED, exception)

    return json(dict(data=trapped_exceptions))


@app.exception(RequestTimeout)
def timeout(request, exception):
    return text('RequestTimeout from error_handler.', 408)


@app.listener('before_server_start')
def init_graphql(app, loop):
    app.add_route(
        GraphQLCompatibilityWrapper.as_view(
            schema=schema, executor=AsyncioExecutor(loop=loop), graphiql=False
        ),
        '/graphql'
    )
    app.add_route(
        GraphQLCompatibilityWrapper.as_view(
            schema=schema, executor=AsyncioExecutor(loop=loop), graphiql=True
        ),
        '/graphiql'
    )
    static_path = pkg_resources.resource_filename(__name__, '../crudl/static')
    app.static('/static', static_path, use_modified_since=configuration.use_modified_since)
    app.static('/favicon.ico', '{}/favicon.ico'.format(static_path), use_modified_since=configuration.use_modified_since)


# @app.route("/")
# async def admin(request):
#     return jinja.render('admin/index.html', request, config=configuration)


@app.route('crudl-graphql/<entity>/<id>')
async def admin(request, entity, id):
    return jinja.render('admin/index.html', request, config=configuration)

@app.route('crudl-graphql/<entity>')
async def admin(request, entity):
    return jinja.render('admin/index.html', request, config=configuration)

@app.route('crudl-graphql/')
async def admin(request):
    return jinja.render('admin/index.html', request, config=configuration)


@app.post('/rest-api/login/')
async def login(request):
    LOG.debug('login %r' % request.json)
    return json({'token': '--tkn-', 'user': 'Gordon Elliott', 'username': 'ge'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
