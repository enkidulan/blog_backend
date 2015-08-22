import colander
import deform.widget

from persistent import Persistent

from substanced.content import content
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer


class CollectionSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        )
    text = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )
    content_type = colander.SchemaNode(
       colander.String(),
       )
    path = colander.SchemaNode(
       colander.String(),
       )
    sort_field = colander.SchemaNode(
       colander.String(),
       default='pubdate',
       )
    sort_inverse = colander.SchemaNode(
       colander.Bool(),
       default=False,
       )
    total_results = colander.SchemaNode(
       colander.Int(),
       default=10,
       )


class CollectionPropertySheet(PropertySheet):
    schema = CollectionSchema()


@content(
    'Collection',
    icon='glyphicon glyphicon-align-left',
    add_view='add_collection',
    propertysheets=(
        ('Basic', CollectionPropertySheet),
    ),
)
class Collection(Persistent):

    name = renamer()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
