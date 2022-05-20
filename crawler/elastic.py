from urllib.parse import urlparse
from elasticsearch import Elasticsearch
import logging
import copy
from scrapy.exceptions import CloseSpider


class Elastic():
    def __init__(self, hosts, http_auth, indices, content_type_settings):
        self.client = Elasticsearch(hosts=hosts, http_auth=http_auth)
        self.indices_client = self.client.indices
        self.indices_list = indices
        self.content_type_settings = content_type_settings

        # TODO: Make debug logging only applicable while on development environment!
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        try:
            if not self.client.ping():
                raise ValueError(
                    "Client failed to connect to the cluster.")

            for index in self.indices_list:
                if not self._is_existing_index(index):
                    self.logger.info(
                        f"Index {index} does no exist! Attempting to create index.")
                    self._create_index(index)
                    
        except Exception as e:
            self.logger.error(f"Elasticsearch init failed.", exc_info=True)
            self.client = None
            self.indices_client = None

    def _create_index(self, index_name):
        try:
            if not self.indices_client.create(index_name):
                raise ValueError(
                    f"Failed to create a new index with name {index_name}.")
            else:
                self.logger.info(f"Index {index_name} created.")
        except Exception as e:
            self.logger.error(
                f"Elasticsearch index creation failed.", exc_info=True)

    def _is_existing_index(self, index_name):
        try:
            if self.indices_client.exists(index_name):
                self.logger.debug(
                    f"Index {index_name} exist check successful.")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(
                f"Elasticsearch failed to check index existence.", exc_info=True)

    def index_document(self, website_data, index_name):
        self.parse_classification(website_data)
        self.format_document(website_data) 
        self._add_suggest_fields(website_data)
        self._remove_duplicates(website_data)
        response = self.client.index(index=index_name, body=website_data,
                          doc_type='_doc', id=website_data['domain_path'])
        return True if response['result'] == 'created' or response['result'] == 'updated' else False

    def is_existing_document(self, id, hash, index_name):
        query = {
            "term": {
                "_id": {
                    "value": id
                }
            }
        }

        fields = ["domain_path", "hash"]

        response = self.client.search(index=index_name, query=query,
                                      fields=fields, _source=False, doc_type='_doc')['hits']['hits']
        # self.logger.debug(response)

        if response != [] and response[0]['fields']['hash'][0] == hash:
            return True
        else:
            return False

    # Themes: kasvatus ja koulutus, varhaiskasvatus ...
    # Content type: uutinen, yhteystieto... oletus tietosivu
    def parse_classification(self, website_data):
                
        # CONTENT TYPE
        # TODO: Get content type from element inside of head section
        ct = None
        if(self.content_type_settings['settings']['parse_content_type_from'] == 'url'):
            url_path_sections = copy.copy(self._get_path_sections(website_data['url']))
            ct = self._get_content_type_from_array(url_path_sections)            
        
        elif(self.content_type_settings['settings']['parse_content_type_from'] is not None):
            try:
                breadcrumb = copy.copy(website_data['body'][self.content_type_settings['settings']['parse_content_type_from']])
                if(type(breadcrumb) is list):
                    breadcrumb = self._clean_breadcrumb(breadcrumb)
                    ct = self._get_content_type_from_array(breadcrumb)
                elif(type(breadcrumb) is str):
                    ct = self._get_content_type_from_array([breadcrumb])
            except KeyError as ke:
                self.logger.error(f"Incorrect configuration in 'CONTENT_TYPES_AND_THEMES' section: {ke}", exc_info=True)        
            
        if(ct):
            website_data['content_type'] = ct

        if('content_type' not in website_data):
            website_data['content_type'] = self.content_type_settings['settings']['default_content_type']

        # THEME
        themes = None
        if(self.content_type_settings['settings']['parse_themes_from'] == 'url'):
            url_path_sections = copy.copy(self._get_path_sections(website_data['url'], self.content_type_settings['settings']['remove_last_part_from_url'] == True))
            themes = url_path_sections
        
        elif(self.content_type_settings['settings']['parse_themes_from'] is not None):
            breadcrumb = copy.copy(website_data['body'][self.content_type_settings['settings']['parse_themes_from']])
            if(type(breadcrumb) is list):
                breadcrumb = self._clean_breadcrumb(breadcrumb, self.content_type_settings['settings']['remove_last_part_from_breadcrumb'] == True)
                themes = breadcrumb
            elif(type(breadcrumb) is str):
                themes = [breadcrumb]
            
        if(themes):
            website_data['themes'] = themes
        else:
            website_data['themes'] = []

        
    def _get_path_sections(self, url, remove_last_part=False):
        parsedUrl = urlparse(url)
        path_sections = parsedUrl[2].split('/') # first is empty, last one is the page itself
        if(len(path_sections) > 1):
            path_sections.pop(0)
        if(len(path_sections) > 1 and remove_last_part):
            path_sections.pop()
        
        return path_sections

    def _clean_breadcrumb(self, breadcrumb, remove_last_part=False):
        if(len(breadcrumb) > 1 and self.content_type_settings['settings']['remove_first_part_from_breadcrumb'] == True):
            breadcrumb.pop(0)
        if(len(breadcrumb) > 1 and remove_last_part):
            breadcrumb.pop()
        
        return breadcrumb

    def _get_content_type_from_array(self, arr):
        for x in arr:
            for key, types in self.content_type_settings.items():
                if(key == 'settings'): continue
                if(types and x.lower() in types):
                    return key


    # Map fields from index to the display_fields section in the index
    def format_document(self, website_data):
        display_fields = self.content_type_settings['settings']['display_fields']
        for key, value in display_fields.items():
            if(value):                
                field_settings = self._get_field_settings(value)
                if(value['index_fields']):
                    index_fields_length = len(value['index_fields'])
                    for x in range(index_fields_length):
                        if(x < index_fields_length):                            
                            try:               
                                data_value = self._find_key_from_data(value['index_fields'][x], website_data)
                                if(data_value != None): 
                                    if(key not in website_data):
                                        website_data[key] = data_value
                                    elif(field_settings['append']):
                                        website_data[key].extend(data_value)                                
                            except Exception as e:
                                raise CloseSpider(reason="Elasticsearch client failure {e}") # todo: Stops crawling with decent message?
                            if(x == index_fields_length-1):
                                if(key not in website_data or website_data[key] is None):
                                    website_data[key] = field_settings['default']
                else:
                    website_data[key] = field_settings['default']
            else:
                website_data[key] = []

    def _get_field_settings(self, value):
        default_value = []
        val = copy.copy(value)
        if('default' in val and val['default'] is not None):
            default_value = [val['default']]
        if('append_values' in val and val['append_values'] == True):
            append_values = True
        else:
            append_values = False
        val.pop('default', None)
        val.pop('append_values', None)
        return {
            'default': default_value,
            'append': append_values
            }

    def _find_key_from_data(self, key, website_data):        
        if('head' in website_data and key in website_data['head']):
            return copy.copy(website_data['head'][key])            
        elif('body' in website_data and key in website_data['body']):
           return copy.copy(website_data['body'][key])
        elif(key in website_data):
            return copy.copy(website_data[key])

    # Removes duplicate values from each key in website_data
    def _remove_duplicates(self, website_data):
        for key in website_data:
            if(type(website_data[key]) == list):
                website_data[key] = list(dict.fromkeys(website_data[key]))

    # Add configured fields to the field used in the search suggestion
    def _add_suggest_fields(self, website_data):
        outwords = []
        # 1. for each configured item take each of the phrases and insert those as the suggested items. 
        # 2. Add each single word also as a separate suggestion
        # 3. Add each phrase with the first word removed as a separate suggestion 
        # Does not remove duplicates (those should be (and are) removed separately)
        # Example: phrase: 'word1 word2 word3 word4' --> ['word1 word2 word3 word4', 'word1', 'word2', 'word3', 'word4', 'word2 word3 word4', 'word3 word4']
        
        for k, v in self.content_type_settings['settings']['display_fields'].items():
            if('suggest' in v.keys() and v['suggest']):
                # split words by whitespace and add each without the first one
                words = website_data[k]
                outwords.extend(words) 
                for phrase in words:                    
                    
                    w = phrase.split(' ')
                    
                    outwords.extend(w) # jokainen erillinen sana

                    # Add 
                    while w:
                        del w[0]
                        end = ' '.join(w)
                        if(len(end) > 1):
                            outwords.insert(len(outwords), end)
                            

        website_data['suggest'] = outwords
