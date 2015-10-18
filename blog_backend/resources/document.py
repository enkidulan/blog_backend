import colander
import deform.widget
import datetime

from persistent import Persistent

from substanced.content import content
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer


# def context_is_a_document(context, request):
#     return request.registry.content.istype(context, 'Document')


@colander.deferred
def now_default(node, kw):
    return datetime.datetime.now()


@colander.deferred
def get_author_name(node, kw):
    return kw['request'].authenticated_userid


class BaseDocumentSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        )
    description = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )
    text = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )
    pubdate = colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        default=now_default,
        )


class MetadataSchema(Schema):

    keywords = colander.SchemaNode(
        colander.String(),
        default=tuple(),
        )
    author = colander.SchemaNode(
        colander.String(),
        default=get_author_name,
        )
    short_description = colander.SchemaNode(
        colander.String(),
        default='',
        )


class DocumentSchema(BaseDocumentSchema, MetadataSchema):

    @staticmethod
    def propertysheets():
        class MetadataPropertySheet(PropertySheet):
            schema = MetadataSchema()

        class DocumentPropertySheet(PropertySheet):
            schema = BaseDocumentSchema()

        return (
            ('Basic', DocumentPropertySheet),
            ('Metadata', MetadataPropertySheet),
        )


@content(
    'Document',
    icon='glyphicon glyphicon-align-left',
    add_view='add_document',
    catalog=True,
    propertysheets=DocumentSchema.propertysheets()
)
class Document(Persistent):

    name = renamer()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
