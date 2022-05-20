from src.config_model import ValidationModel
from pydantic import ValidationError
import pytest

@pytest.fixture
def empty_config():
    return {}

@pytest.fixture
def bad_config():
    return {}

@pytest.fixture
def good_config():
    return {
        'backend': {
            'analytics': {
                'value_1': "value_str",
                'value_2': {
                    'value_key_1': "value_str_1",
                    'value_key_2': "value_str_2"
                },
                'value_3': None
            }
        },
        'elasticsearch': {
            'hosts': ["host_1", "host_2"],
            'index_prefix': "prefix_string_value",
            'index_reader_rolename': "reader_rolename_value",
            'index_writer_rolename': "writer_rolename_value",
            'languages': ["fi", "sv", "en"],
            'analyzers': {
                'default': {
                    'tokenizer': "standard",
                    'token_filters': ["lowercase", {'type': "stop", 'stopwords': ["_finnish_"]}]
                },
                'fi':{
                    'some_analyzer_name': {
                        'char_filters': None,
                        'tokenizer': "standard",
                        'token_filters': ["lowercase", {'type': "stop", 'stopwords': ["_finnish_"]}]
                    }
                }
            },
            'search_settings':{
                'field_boosts': {
                    'some_name_1': {
                        'field': "field_name",
                        'values': "value_string",
                        'boost': 2
                    },
                    'some_name_2': {
                        'field': "field_name",
                        'values': ["value_1", "value_2"],
                        'boost': 1.8
                    }
                }
            },
            'suggest_settings': {
                'some_name': {
                    'completion': {
                        'field': "suggest",
                        'skip_duplicates': True,
                        'fuzzy': {
                            'fuzziness': 0
                        },
                        'size': 20
                    }
                }
            }
        },
        'SCRAPY_SETTINGS': {
            'GENERAL':{
                'DEPTH_LIMIT': 0,
                'DOWNLOAD_DELAY': 1.0,
                'DOWNLOAD_TIMEOUT': 10,
                'LOG_ENABLED': True,
                'LOG_FILE': None,
                'LOG_FORMAT': "some_format_string",
                'LOG_LEVEL': 'INFO',
                'LOGSTATS_INTERVAL': 60,
                'ROBOTSTXT_OBEY': True
            },
            'SPIDERS': {
                'SomeSpiderName': {
                    'BOT_NAME': "some_name",
                    'ALLOWED_DOMAINS': ["www.somedomain.com"],
                    'START_URLS': ["www.somedomain.com"],
                    'LINK_EXTRACTOR_RULES': {
                        'allow': ["/path_string_1", "/path_string_2"],
                        'deny': None
                    },
                    'CUSTOM_SETTINGS': {
                        'CRAWL_LINKS_ONLY': ["/path/"],
                        'REPLACE_CHARACTERS': {
                            "some_string": "replacing_string"
                        },
                        'ITEM_PIPELINES': {
                            'generic.generic.pipelines.NLPPipeline': 300,
                            'generic.generic.pipelines.ElasticsearchPipeline': 500
                        },
                        'NLP_SETTINGS': {
                            'nlp_api_address': "http://host.docker.internal:15000",
                            'nlp_dictionary_path': "/usr/share/elasticsearch/config/nlp_dictionary_fi.txt"
                        },
                        'SCRAPER_SETTINGS': {
                            'lang': {'url': {'path': 0}},
                            'head': None,
                            'body': {
                                'element': "div",
                                'class': "some_class",
                                'id': None,
                                'exclude_rules': {
                                    'ruleset1': {
                                        'element': "div",
                                        'class': "non-public",
                                        'id': None
                                    }
                                },
                                'content_to_scrape': {
                                    'field_1': {
                                        'element': "div",
                                        'attributes': {
                                            'class': "some_class_1",
                                            'id': None
                                        },
                                        'indexing': None,
                                        'search': None
                                    },
                                    'field_2': {
                                        'element': "div",
                                        'attributes': {
                                            'class': "some_class_1",
                                            'id': None
                                        },
                                        'indexing': None,
                                        'search': None
                                    },
                                    'field_3_img': {
                                        'element': "div",
                                        'attributes': {
                                            'class': "some_class_2",
                                            'id': None
                                        },
                                        'image': {
                                            'target_element': "div",
                                            'target_attributes': {
                                                'class': None,
                                                'id': "some_id_1"
                                            },
                                            'content_attribute': "src",
                                            'alt_text': "alt",
                                            'title': "title"
                                        }
                                    }
                                }
                            }
                        },
                        'CONTENT_TYPES_AND_THEMES': {
                            'settings': {
                                'parse_content_type_from': "url",
                                'parse_themes_from': "breadcrumb",
                                'default_content_type': "tietosivu",
                                'remove_last_part_from_url_path': True,
                                'remove_first_part_from_breadcrumb': True,
                                'remove_last_part_from_breadcrumb': True,
                                'display_fields': {
                                    'title': {
                                        'default': "",
                                        'append_values': True,
                                        'index_fields': ["field_1", "field_2"],
                                        'suggest': True
                                    },
                                    'text': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'publish_date': {
                                        'default': "Jotain",
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'modify_date': {
                                        'append_values': False,
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'writer': {
                                        'append_values': True,
                                        'index_fields': ["field_1", "field_2"],
                                        'suggest': False
                                    },
                                    'location': {
                                        'index_fields': ["field_1", "field_2"],
                                        'suggest': False
                                    },
                                    'date': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'time': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'url': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'image_url': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'keywords': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'content_type': {
                                        'index_fields': ["field_1", "field_2"],
                                    },
                                    'themes': {
                                        'index_fields': ["field_1", "field_2"],
                                    }
                                }
                            },
                            'tietosivu': None,
                            'uutinen': ["uutinen", "uutiset"],
                            'yhteystieto': ["yhteystieto"],
                            'tapahtuma': ["tapahtumat"],
                            'palvelu_tai_asiointikanava': ["palvelu", "palvelut", "asiointikanava", "service"]
                        }
                    }
                }
            }
        }
    }

def test_config_model_with_empty_config(empty_config):
    with pytest.raises(ValidationError):
        ValidationModel.parse_obj(empty_config)

def test_config_model_with_good_config(good_config):
    error = None
    try:
        ValidationModel.parse_obj(good_config)
    except ValidationError as e:
        error = e

    assert error == None

def test_config_model_with_bad_config(bad_config):
    with pytest.raises(ValidationError):
        ValidationModel.parse_obj(bad_config)