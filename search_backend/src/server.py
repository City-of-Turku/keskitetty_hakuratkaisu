from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from es import ElasticsearchClient
from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, abort
from flask_apispec import marshal_with
from flask_apispec.annotations import use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_cors import CORS
from os import environ
from search_schema import SearchAPIRequestSchema, SearchResultsSchema, SuggestAPIRequestSchema, SuggestResultSchema, ConfigResultSchema
import utils

app = Flask(__name__)
api = Api(app)
# TODO: Configure CORS
CORS(app)

print(f"Starting search server")

# Configs
config_path = '../../config.yaml'
config = utils.read_config(config_path)

es_config = config['elasticsearch']
spider_configs = config["SCRAPY_SETTINGS"]["SPIDERS"]

# Credentials
elastic_username = environ.get('elastic_read_username')
elastic_password = environ.get('elastic_read_password')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='KeskitettyHakuratkaisu',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

indices = []
for language in es_config['languages']:
    indices.append(f"{es_config['index_prefix']}-{language}")

client = ElasticsearchClient(
    hosts=es_config['hosts'],
    http_auth=(elastic_username, elastic_password),
    indices=indices,
    index_prefix=es_config['index_prefix'],
    default_lang=es_config['languages'][0],
    languages=es_config['languages']
)

client.create_query_statements(es_config['search_settings'], es_config['suggest_settings'], spider_configs)
ui_configs = utils.get_ui_configs(config)

class Ping(MethodResource, Resource):
    def get(self):
        try:
            if client.ping():
                return "Connection OK"
            else:
                abort(503)
        except Exception as e:
            print(f"Ping failed: {e}")
            abort(500)
api.add_resource(Ping, '/ping')
docs.register(Ping)

class SearchAPI(MethodResource, Resource):
    @use_kwargs(SearchAPIRequestSchema, location=('json'))
    @marshal_with(SearchResultsSchema, description="Search result object")
    def post(self, **kwargs):
            result = client.search(kwargs)
            if result:
                if 'error' in result:
                    # This is a fallback. Schema handles normal validation errors directly.
                    return jsonify(result), 400
                return jsonify(result)
api.add_resource(SearchAPI, '/search')
docs.register(SearchAPI)

class SuggestAPI(MethodResource, Resource):
    @use_kwargs(SuggestAPIRequestSchema, location=('json'))
    @marshal_with(SuggestResultSchema, description="Suggest result object")
    def post(self, **kwargs):
            result = client.suggest(kwargs)
            if result:
                return jsonify(result)
            else:
                abort(500)
api.add_resource(SuggestAPI, '/suggest')
docs.register(SuggestAPI)


class ConfigAPI(MethodResource, Resource):
    @marshal_with(ConfigResultSchema, description="Configuration result object")
    def get(self):        
        result = ui_configs
        if result:
            return jsonify(result)
        else:
            abort(500)
api.add_resource(ConfigAPI, '/config')
docs.register(ConfigAPI) 

if __name__ == "__main__":
    app.run(host='0.0.0.0')
