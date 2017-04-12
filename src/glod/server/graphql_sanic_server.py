__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException, RequestTimeout
from sanic_graphql import GraphQLView

from a_tuin.db.metadata import metadata
from a_tuin.db.session_scope import Session
from glod.db.engine import engine

from glod.api.schema import schema


app = Sanic(__name__)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    request['session'] = Session()


@app.middleware('response')
async def commit_session(request, response):
    # after each request commit and close the session
    request['session'].commit()
    request['session'].close()


@app.exception(SanicException)
def rollback_session(request, exception):
    request['session'].rollback()
    request['session'].close()
    return app.error_handler.default(request, exception)


@app.exception(RequestTimeout)
def timeout(request, exception):
    return text('RequestTimeout from error_handler.', 408)


@app.route("/")
async def test(request):
    return text('Glod Dev Server')


app.add_route(GraphQLView.as_view(schema=schema, graphiql=True), '/graphql')


if __name__ == '__main__':
    metadata.create_all(engine)
    app.run(host="0.0.0.0", port=8000, debug=True)
