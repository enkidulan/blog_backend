from pyramid.renderers import get_renderer
from pyramid.renderers import render_to_response
from pyramid.view import view_config, render_view
from ..resources.document import Document
from ..resources.collection import Collection

# from pyramid.traversal import resource_path
from substanced.util import find_catalog
from operator import attrgetter


class BaseJSONYView():
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def response(self):
        raise NotImplemented()

    def __call__(self):
        return render_to_response('json', self.response(), self.request)


@view_config(context=Document)
class DocumetView(BaseJSONYView):

    def response(self):
        return {
            'title': self.context.title,
            'description': self.context.description,
            'text': self.context.text,
            'pubdate': self.context.pubdate.strftime('%Y-%m-%d %H:%M:%S'),
            'keywords': self.context.keywords,
            'author': self.context.author,
            'short_description': self.context.short_description,
        }


@view_config(context=Collection)
class CollectionView(BaseJSONYView):

    def response(self):
        catalog = find_catalog(self.context, 'system')
        content_type = catalog['content_type']
        query = content_type.eq(self.context.target_content_type)
        if self.context.path is not None:
            path = catalog['path']
            query &= path.eq(self.context.path, include_origin=False)
        resultset = [i for i in query.execute()]
        resultset.sort(
            key=attrgetter(self.context.sort_field),
            reverse=self.context.sort_inverse)
        resultset = [str(render_view(e, self.request)) for e in resultset]
        return {
            'title': self.context.title,
            'text': self.context.text,
            'items': resultset[:self.context.total_results or None],
        }

