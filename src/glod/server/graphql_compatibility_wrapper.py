__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

from sanic_graphql import GraphQLView


class GraphQLCompatibilityWrapper(GraphQLView):

    async def get(self, request, *args, **kwargs):
        return self.dispatch_request(request, *args, **kwargs)

    async def put(self, request, *args, **kwargs):
        return self.dispatch_request(request, *args, **kwargs)

    async def post(self, request, *args, **kwargs):
        return self.dispatch_request(request, *args, **kwargs)

    async def delete(self, request, *args, **kwargs):
        return self.dispatch_request(request, *args, **kwargs)
