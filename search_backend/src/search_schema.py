from marshmallow import Schema, fields
from marshmallow import validate
from marshmallow.exceptions import ValidationError
from marshmallow.validate import ContainsOnly, OneOf
import utils

# Configs
config_path = '../../config.yaml'
config = utils.read_config(config_path)
es_config = config['elasticsearch']
languages = es_config['languages']

class SearchAPIRequestSchema(Schema):
    def validate_filters(filters):
        if len(filters) == 0:
            return True
        for key, value in filters.items():
            if '!' in value:
                raise ValidationError(message=f"Filter {key} contained an illegal value.")

    search_term = fields.String(required=True, description="Search term or phrase")
    page_index = fields.Integer(required=False, strict=True, description="The index number of the first result returned")
    per_page = fields.Integer(required=False, strict=True, description="The number of results returned per page")
    language = fields.String(required=False, strict=True, description="The language tag of the search (e.g. 'fi', 'sv' or 'en')", validate=OneOf(languages, error="Invalid language code."))
    filters = fields.Dict(validate=validate_filters, required=False, description="Search filter object. Key-value pairs with field name as the key and accepted value as a string or multiple values as an array of strings. (e.g. 'content_type': 'uutinen' or 'content_type': ['uutinen', 'yhteystieto'])")

class SuggestAPIRequestSchema(Schema):
    search_term = fields.String(required=True, description="Search term or phrase")
    language = fields.String(required=False, strict=True, description="The language tag of the search (e.g. 'fi', 'sv' or 'en')", validate=OneOf(languages, error="Invalid language code."))

class HitSource(Schema):
    url = fields.URL()
    head = fields.Dict(keys=fields.String(), values=fields.String())
    body = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))
    hash = fields.String()

class Hit(Schema):
    _id = fields.String()
    _index = fields.String()
    _score = fields.Float()
    _ignored = fields.List(fields.String())
    _source = fields.Nested(HitSource)
    _type = fields.String()
    highlight = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))
    fields = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))

class SearchMetadata(Schema):
    total_count = fields.Integer()
    page_index = fields.Integer()
    per_page = fields.Integer()
    page_number = fields.Integer()
    page_count = fields.Integer()
    first_page = fields.Integer()
    next_page = fields.Integer()
    previous_page = fields.Integer()
    last_page = fields.Integer()
    took = fields.Integer()

class SearchResult(Schema):
    hits = fields.List(fields.Nested(Hit))
    metadata = fields.Nested(SearchMetadata)

class SearchResultsSchema(Schema):
    primary = fields.Nested(SearchResult)
    secondary = fields.Nested(SearchResult)
    errors = fields.String()

# SUGGEST
# Single suggest 'hit'
class Suggestion(Schema):
    text = fields.String(description="Suggested text based on the search term")
    _index = fields.String()
    _type = fields.String()
    _id = fields.String()
    _score = fields.Float()
    _ignored = fields.List(fields.String())

# Single resultset for suggest
class Suggest(Schema):
    text = fields.String()
    offset = fields.Integer()
    length = fields.Integer()
    options = fields.Nested(Suggestion)

# Suggest wrapper
class SuggestResponse(Schema):
    suggest = fields.Nested(Suggest)

class SuggestMetadata(Schema):
    took = fields.Integer()

class SuggestResultSchema(Schema):
    metadata = fields.Nested(SuggestMetadata)
    suggest = fields.List(fields.Nested(SuggestResponse))

# CONFIG
class ConfigResultSchema(Schema):
    languages = fields.List(fields.String())
    content_types = fields.List(fields.String())
    analytics = fields.Dict()
