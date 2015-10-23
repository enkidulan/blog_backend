import logging

from substanced.folder import Folder
from blog_backend.resources.collection import Collection
from blog_backend.resources.document import Document
from datetime import datetime

_marker = object()

logger = logging.getLogger('evolution')


def safe_objects_creator(context, name, constructor, kwparams):
    obj = getattr(context, name, _marker)
    logger.info('Creating folder for blog posts')
    if obj is not _marker:
        return
    context[name] = constructor(**kwparams)


def create_blog_structure(root):
    logger.info('Creating basic content structure for blog')
    # import pdb; pdb.set_trace()
    safe_objects_creator(root, 'blog_posts', Folder, {})
    # safe_objects_creator(root['blog_posts'], 'first_post', Document, {
    #     'title': 'Firs Blog Post',
    #     'body': 'Welcome to simple substanced blog :)',
    #     'pubdate': datetime.now(),
    # })
    safe_objects_creator(root, 'blog', Collection, {
        'title': 'Blog',
        'text': 'Collection for displaying blog posts',
        'target_content_type': 'Document',
        'path': '/blog_posts',
        'sort_field': 'pubdate',
        'sort_inverse': True,
        'total_results': 1,
    })


def includeme(config):
    config.add_evolution_step(create_blog_structure)
