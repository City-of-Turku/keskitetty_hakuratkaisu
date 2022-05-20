# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from elastic import Elastic
from scrapy.exceptions import CloseSpider, DropItem
import logging
import os

class ElasticsearchPipeline:

    def open_spider(self, spider):
        self.logger = logging.getLogger(__name__)
        self.es_config = spider.es_config
        self.index_prefix = self.es_config['index_prefix']

        self.indices = []
        for language in self.es_config['languages']:
            self.indices.append(f"{self.index_prefix}-{language}")

        auth = (os.environ.get('elastic_write_username'), os.environ.get('elastic_write_password'))

        self.es = Elastic(
            hosts=self.es_config["hosts"],
            http_auth=auth,
            indices=self.indices,
            content_type_settings=spider.settings.get("CONTENT_TYPES_AND_THEMES")
        )
        
        if not self.es.client:
            raise CloseSpider(reason="Elasticsearch client failure")


    def process_item(self, item, spider):
        if item['lang'] not in self.es_config['languages']:
            raise DropItem(f'Dropped item for undefined language "{item["lang"]}"')
            
        target_index = f'{self.index_prefix}-{item["lang"]}'
        
        if self.es.is_existing_document(item['domain_path'], item['hash'], target_index):
            self.logger.info(f"Existing document: {item['domain_path']}")
        elif self.es.index_document(item, target_index):
            self.logger.info(
                f"Indexed new document: {item['domain_path']}")
        else:
            self.logger.error(f"Indexing failed: {item}")
            raise DropItem(f"Dropped item for failing indexing")

        return item


from nlp_client import NLPProcessorClient

class NLPPipeline:
    def open_spider(self, spider):
        try:
            nlp_settings = spider.settings.get("NLP_SETTINGS")
            nlp_api_address = nlp_settings['nlp_api_address'] if 'nlp_api_address' in nlp_settings.keys() and nlp_settings['nlp_api_address'] and len(nlp_settings['nlp_api_address']) > 0 else 'http://localhost:15000'
            nlp_dictionary_path = nlp_settings['nlp_dictionary_path'] if 'nlp_dictionary_path' in nlp_settings.keys() and nlp_settings['nlp_dictionary_path'] and len(nlp_settings['nlp_dictionary_path']) > 0 else './elasticsearch/nlp_dictionary.txt'
            
            spider.nlp = NLPProcessorClient(nlp_api_address, nlp_dictionary_path)
        except Exception as e:
            raise CloseSpider(reason='NLP client failure.')

    def close_spider(self, spider):
        del spider.nlp

    def process_item(self, item, spider):
        if item['lang'] != 'fi':
            return item

        content = item['body']['full_content']
        if content and len(content) > 0:
            spider.nlp.process(content)
        
        return item

class SynonymGatheringPipeline:
    def open_spider(self, spider):
        try:
            synonym_settings = spider.settings.get("SYNONYM_SETTINGS")
            spider.synonym_filepath = synonym_settings['filepath'] if 'filepath' in synonym_settings.keys() and synonym_settings['filepath'] and len(synonym_settings['filepath']) > 0 else './elasticsearch/synonyms.txt'
            spider.bidirectional = synonym_settings['bidirectional'] if 'bidirectional' in synonym_settings.keys() and synonym_settings['bidirectional'] != None else False
            with open(spider.synonym_filepath, 'at', encoding='utf-8'):
                print('Synonym file ready.')
        except:
            raise CloseSpider(reason='Failed to initialize SynonymGatheringPipeline.')

    def process_item(self, item, spider):
        connector_symbol = ", " if spider.bidirectional else " => "
        base_terms = ""
        synonyms = ""
        
        for element in (item['head'], item['body']):
            for key, term_lst in element.items():
                for term in term_lst:
                    if (key.startswith('word') and base_terms.find(term.lower()) == -1):
                        base_terms += ', ' + term.lower() if len(base_terms) > 0 else term.lower()
                    if (key.startswith('synonym') and synonyms.find(term.lower()) == -1):
                        synonyms += ', ' + term.lower() if len(synonyms) > 0 else term.lower()

        if (len(synonyms) > 1):
            synonym_clause = ""
            if (len(base_terms) > 0):
                synonym_clause = base_terms + connector_symbol + synonyms
            elif (spider.bidirectional):
                synonym_clause = synonyms
            else:
                return item

            with open(spider.synonym_filepath, 'rt+', encoding='utf-8') as file:
                existing = file.read()
                if (existing.find(synonym_clause) != -1):
                    return item
                else:
                    file.write(synonym_clause + '\n')
        
        return item