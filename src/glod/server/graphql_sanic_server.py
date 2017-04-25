__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""
import logging
import pkg_resources

from sanic import Sanic
from sanic.response import text, json
from sanic.exceptions import SanicException, RequestTimeout
from sanic_graphql import GraphQLView
from sanic_jinja2 import SanicJinja2, PackageLoader

from a_tuin.constants import SESSION
from a_tuin.db.metadata import metadata
from a_tuin.db.session_scope import Session
from glod.db.engine import engine
from glod.configuration import configuration
from glod.api.schema import schema


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
    # after each request commit and close the session
    request[SESSION].commit()
    request[SESSION].close()


@app.exception(SanicException)
def rollback_session(request, exception):
    request[SESSION].rollback()
    request[SESSION].close()
    return app.error_handler.default(request, exception)


@app.exception(RequestTimeout)
def timeout(request, exception):
    return text('RequestTimeout from error_handler.', 408)

static_path = pkg_resources.resource_filename(__name__, '../crudl/static')
app.static('/static', static_path, use_modified_since=configuration.use_modified_since)
app.static('/favicon.ico', '{}/favicon.ico'.format(static_path), use_modified_since=configuration.use_modified_since)


# @app.route("/")
# async def admin(request):
#     return jinja.render('admin/index.html', request, config=configuration)


@app.route('crudl-graphql/')
async def admin(request):
    return jinja.render('admin/index.html', request, config=configuration)


@app.post('/rest-api/login/')
async def login(request):
    LOG.debug('login %r' % request.json)
    return json({'token': '--tkn-', 'user': 'Gordon Elliott', 'username': 'ge'})


app.add_route(GraphQLView.as_view(schema=schema, graphiql=False), '/graphql')
app.add_route(GraphQLView.as_view(schema=schema, graphiql=True), '/graphiql')


if __name__ == '__main__':
    metadata.create_all(engine)
    app.run(host="0.0.0.0", port=8000, debug=True)
