from pyramid.renderers import get_renderer
from pyramid.renderers import render_to_response
from pyramid.view import view_config, render_view
from ..resources.document import Document
from ..resources.collection import Collection

# from pyramid.traversal import resource_path
from substanced.util import find_catalog
from operator import attrgetter
from substanced.principal import DefaultUserLocator


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
        # import pdb; pdb.set_trace()
        adapter = DefaultUserLocator(self.context, self.request)
        user = adapter.get_user_by_userid(int(self.context.author))
        return {
            'title': self.context.title,
            'description': self.context.description,
            'text': self.context.text,
            'pubdate': self.context.pubdate.strftime('%Y-%m-%d %H:%M:%S'),
            'keywords': self.context.keywords,
            'author': user.name,
            'short_description': self.context.short_description,
        }


@view_config(context=Collection)
class CollectionView(BaseJSONYView):

    def response(self):
        page = int(self.request.params.get('page') or 0)
        description_only = self.request.params.get('description_only', False)

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
        if description_only:
            resultset = [
                {'title': e.title,
                 'name': e.name,
                 'description': e.short_description}
                for e in resultset]
            page_to_show = slice(None)
        else:
            resultset = [str(render_view(e, self.request)) for e in resultset]
            page_to_show = slice(page, page + self.context.total_results or None)
        return {
            'title': self.context.title,
            'text': self.context.text,
            'items': resultset[page_to_show],
            'page': page,
            'pages': len(resultset),
        }
