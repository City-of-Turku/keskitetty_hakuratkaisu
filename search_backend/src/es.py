from elasticsearch import Elasticsearch
import es_tools
import traceback

# Elasticsearch indexing and searching functionalities


class ElasticsearchClient:

    def __init__(self, hosts, http_auth, indices, index_prefix, default_lang, languages):
        self.client = Elasticsearch(
            hosts=hosts,
            http_auth=http_auth
        )
        self.indices_client = self.client.indices
        self.indices = indices
        self.index_prefix = index_prefix
        self.default_lang = default_lang
        self.languages = languages
        self.query = None
        self.highlight = None
        self.fields = None
        self.suggestQuery = None
        try:
            if not self.client.ping(request_timeout=10):
                raise ValueError("Elasticsearch init connection failed")
        except Exception as e:
            print('Elasticsearch exception occurred in es.py initialization')
            traceback.print_exc()

    # Elastic Ping
    def ping(self):
        try:
            return self.client.ping()
        except Exception as e:
            print(f'Elasticsearch connection ping failed: {e}')
            return False

    # Elastic Search query
    def search(self, kwargs):
        try:
            page_index = kwargs.get('page_index', 0)
            per_page = kwargs.get('per_page', 10)
            search_term = kwargs.get('search_term', '')
            language = kwargs.get('language', None)
            filters = kwargs.get('filters', dict())

            if language:
                index = f"{self.index_prefix}-{language}" if language in self.languages else None
            else:
                index = f"{self.index_prefix}-{self.default_lang}" if self.default_lang else None

            if index == None:
                return {'error': 'Language code does not exist'}

            results = self.client.msearch(
                body=self._get_query_body(search_term, from_=str(page_index), size=str(per_page), filters=dict(filters)),
                index=index if index else self.indices
            )

            return es_tools.parse_results(results['responses'], page_index, per_page)

        except Exception as e:
            print(f"Search query failed: {e}")
            return None

    # Elastic Suggest query
    def suggest(self, kwargs):
        try:
            search_term = kwargs.get('search_term', '')
            language = kwargs.get('language', None)
            index = f"{self.index_prefix}-{language}" if language else None

            result = self.client.search(
                _source = False,
                suggest=self._get_suggest_object(search_term),
                index=index if index else self.indices,
            )

            response = {
                "suggest": result['suggest'],
                "metadata": {
                    "took": result['took']
                }
            }
            return response
        except Exception as e:
            print(f"Suggesting failed: {e}")
            return None

    def create_indices(self):
        try:
            for index in self.indices:
                if self.indices_client.exists(index):
                    print(f'Creating the index "{index}" failed because it already exists.')
                elif self.indices_client.create(index):
                    print(f'Index "{index}" created successfully.')

            return True
        except Exception as e:
            print(f"Creation of indices failed: {e}")

        return False

    def create_index_template(self, languages, spider_configs, analyzer_settings=None):
        # TODO: Validate the keys of the mapping for allowed values!

        for index in self.indices:
            if self.indices_client.exists(index):
                print(f'Unable to create an index template for prefix "{self.index_prefix}" because index "{index}" already exists.')
                return False

        analyzer_settings = es_tools.parse_analyzer_settings(analyzer_settings)

        indices_mapping_settings = es_tools.parse_index_template_mappings(spider_configs)

        templates = es_tools.get_index_templates(self.index_prefix, languages, indices_mapping_settings, analyzer_settings)

        try:
            for template_name, template in templates.items():
                if not self.indices_client.put_index_template(template_name, body=template):
                    print(f'Creation of index template for index "{template_name}" failed')

            return True
        except Exception as e:
            print(f"Creation of index template failed: {e}")

        return False

    def create_query_statements(self, search_settings, suggest_settings, spider_configs):
        query_field_lst, highlight_obj, display_fields_lst = es_tools.parse_contents_to_scrape(spider_configs)

        fuzziness = search_settings['fuzziness'] if "fuzziness" in search_settings.keys() and search_settings['fuzziness'] else 0
        field_boosts = search_settings['field_boosts'] if "field_boosts" in search_settings.keys() and search_settings['field_boosts'] and len(search_settings['field_boosts']) > 0 else None

        self.query = es_tools.get_query_template(query_field_lst, fuzziness, highlight_obj, display_fields_lst, field_boosts)

        self.suggestQuery = suggest_settings
        self.fields = display_fields_lst

    def _get_query_body(self, search_term="", from_="0", size="10", filters=None):
        query_body = ""

        query_template = self.query

        search_clauses = es_tools.parse_search_term_clauses(search_term)

        filter_str = es_tools.parse_filter_string(filters)

        # Not used if parameter "None"
        post_filter_obj = es_tools.parse_post_filter_object(None)

        for i, clause in enumerate(search_clauses):
            clause_with_filter = clause + filter_str
            query_template = self.query
            query_template = query_template.replace("query_value_str", clause_with_filter)
            query_template = query_template.replace("from_value", from_)
            query_template = query_template.replace("size_value", size)
            query_template = query_template.replace("post_filter_obj", post_filter_obj)

            query_body += query_template
            
            if i < len(search_clauses) - 1:
                query_body += "\n"

        return query_body

    def _get_suggest_object(self, search_term):
        default_suggest_template = {
            "text-suggest": {
                "prefix": f'{search_term}',
                "completion": {
                    "field": "suggest",
                    "skip_duplicates": True,
                    "fuzzy": {
                        "fuzziness": 0
                    }
                }
            }
        }

        if self.suggestQuery:
            for suggestion in self.suggestQuery.keys():
                self.suggestQuery[suggestion]['prefix'] = f'{search_term}'

            suggest_template = self.suggestQuery
        else:
            suggest_template = default_suggest_template

        return suggest_template

    def get_role(self, name):
        try:
            return self.client.security.get_role(name)
        except Exception as e:
            print(f"Getting role failed or role not found: {e}")
            return False

    def put_role(self, name, data):
        try:
            return self.client.security.put_role(name, body=data)
        except Exception as e:
            print(f"Adding role failed: {e}")
            return False

    def put_user(self, username, data):
        try:
            return self.client.security.put_user(username, body=data)
        except Exception as e:
            print(f"Adding user failed: {e}")
            return False