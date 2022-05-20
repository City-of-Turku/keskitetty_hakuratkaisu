from pathlib import Path
from pydantic import BaseModel, conlist, constr, HttpUrl, validator
from typing import Dict, List, Literal, Optional, Union

# This configuration model is formed "backwards".
# The main class is last and it is built on the other partial classes before it.

# Backend conf
class BackendConfig(BaseModel):
    analytics: Union[Dict[constr(min_length=1), Union[constr(min_length=1), dict, None]], None]
# END: Backend conf

# Elasticsearch conf
class FieldBoostSubConfig(BaseModel):
    field: constr(min_length=1)
    values: Union[constr(min_length=1), conlist(constr(min_length=1), min_items=1)]
    boost: Union[int, float]

class SearchSettingsConfig(BaseModel):
    fuzziness: Optional[int]
    field_boosts: Optional[Dict[str, FieldBoostSubConfig]]

class SuggestSettingsConfig(BaseModel):
    field: constr(min_length=1)
    skip_duplicates: bool
    fuzzy: Dict[ Literal['fuzziness'], int ]
    size: int

class AnalyzerSettingsConfig(BaseModel):
    char_filters: Optional[List[Union[constr(min_length=1), Dict[str, Union[str, List[str]]]]]]
    tokenizer: Optional[constr(min_length=1)]
    token_filters: Optional[List[Union[str, dict]]]

class ElasticsearchConfig(BaseModel):
    hosts: conlist(constr(min_length=1), min_items=1)
    index_prefix: constr(min_length=1)
    index_reader_rolename: constr(min_length=1)
    index_writer_rolename: constr(min_length=1)
    languages: conlist(constr(min_length=1), min_items=1)
    analyzers: Dict[Union[Literal['default'], constr(min_length=2, max_length=3)],
        Union[AnalyzerSettingsConfig, Dict[constr(min_length=1), AnalyzerSettingsConfig]]]
    search_settings: SearchSettingsConfig
    suggest_settings: Optional[Dict[str, Dict[
        Literal['completion'], SuggestSettingsConfig
    ]]]

    @validator('analyzers')
    def analyzer_languages_in_languages_list(cls, v, values):
        if 'languages' in values.keys():
            for lang in v:
                if lang == "default":
                    continue
                assert lang in values['languages'], f"Analyzers language '{lang}' was not found on language list."
        else:
            raise ValueError("Languages are missing or not valid. ")
        return v
# END: Elasticsearch conf

# Scrapy conf
class ScrapyIndexingConfig(BaseModel):
    type: Optional[constr(min_length=1)]
    analyzer: Optional[Union[Dict[constr(min_length=2, max_length=3), constr(min_length=1)], None]]
    format: Optional[constr(min_length=1)]

    @validator("analyzer")
    def type_text_check(cls, v, values):
        if "type" in values.keys() and values['type'] != "text":
            raise ValueError("Analyzers can not be used with other field data types than 'text'")
        return v

    @validator("format")
    def format_for_date(cls, v, values):
        if "type" in values.keys() and values['type'] != "date":
            raise ValueError("'format' value can not be given for field data type 'text'")
        return v

class ScrapySearchConfig(BaseModel):
    boost: Optional[Union[int, float]]
    highlight: Optional[Union[bool, dict]]

class ScraperHeadContentToScrapeConfig(BaseModel):
    element: Union[str, None]
    attribute_key_: Union[str, None]
    attribute: Union[str, None]
    attribute_value_: Union[str, None]
    indexing: Union[ScrapyIndexingConfig, None]
    search: Union[ScrapySearchConfig, bool, None]

    class Config:
        fields = {
            'attribute_key_': 'attribute-key',
            'attribute_value_': 'attribute-value'
        }

class ScraperHeadConfig(BaseModel):
    content_to_scrape: Union[Dict[constr(min_length=1), ScraperHeadContentToScrapeConfig], None]

class ScraperExcludeRulesetConfig(BaseModel):
    element: Union[str, None]
    class_: Union[str, None]
    id: Union[str, None]

class ScraperImageConfig(BaseModel):
    target_element: str
    target_attributes: Dict[Literal['class', 'id'], Union[str, None]]
    content_attribute: str
    alt_text: str
    title: str

class ScraperBodyContentToScrapeConfig(BaseModel):
    element: Union[constr(min_length=1), None]
    attributes: Union[Dict[Literal['class', 'id'], Union[constr(min_length=1), None]], None]
    indexing: Union[ScrapyIndexingConfig, None]
    search: Optional[Union[ScrapySearchConfig, bool, None]]
    image: Optional[ScraperImageConfig]

class ScraperBodyConfig(BaseModel):
    element: Union[str, None]
    class_: Union[str, None]
    id_: Union[str, None]
    exclude_rules: Union[Dict[str, ScraperExcludeRulesetConfig], None]
    content_to_scrape: Union[Dict[str, ScraperBodyContentToScrapeConfig], None]

class ScraperDisplayFieldsConfig(BaseModel):
    default: Optional[Union[str, None]]
    append_values: Optional[Union[bool, None]]
    index_fields: Union[List[str], None]
    suggest: Optional[Union[bool, None]]

class ScraperContentTypesAndThemesSettingsConfig(BaseModel):
    parse_content_type_from: str
    parse_themes_from: Union[Literal['url', 'breadcrumb'], None]
    default_content_type: str
    remove_last_part_from_url_path: bool
    remove_first_part_from_breadcrumb: bool
    remove_last_part_from_breadcrumb: bool
    display_fields: Dict[Literal['title', 'text', 'publish_date', 'modify_date', 'writer', 'location', 'date', 'time', 'url', 'image_url', 'keywords', 'content_type', 'themes'], ScraperDisplayFieldsConfig]

class ScraperContentTypeConfig(BaseModel):
    List[str]

class ContentTypesAndThemesConfig(BaseModel):
    settings: ScraperContentTypesAndThemesSettingsConfig
    ScraperContentTypeConfig

class NLPSettingsConfig(BaseModel):
    nlp_api_address: Union[HttpUrl, None]
    nlp_dictionary_path: Union[Path, None]

class SynonymSettingsConfig(BaseModel):
    filepath: Union[Path, None]
    bidirectional: Union[bool, None]

class ScraperSettingsConfig(BaseModel):
    lang: Union[Literal['html'], Dict[Literal['url'], Dict[Literal['path'], int]]]
    head: Union[ScraperHeadConfig, None]
    body: Union[ScraperBodyConfig, None]

class CustomSettingsConfig(BaseModel):
    CRAWL_LINKS_ONLY: Union[List[constr(min_length=1)], None]
    REPLACE_CHARACTERS: Union[Dict[constr(min_length=1), str], None]
    ITEM_PIPELINES: Dict[constr(min_length=1), int]
    NLP_SETTINGS: Union[NLPSettingsConfig, None]
    SYNONYM_SETTINGS: Union[SynonymSettingsConfig, None]
    SCRAPER_SETTINGS: ScraperSettingsConfig
    CONTENT_TYPES_AND_THEMES: ContentTypesAndThemesConfig
    
    @validator('NLP_SETTINGS')
    def nlp_settings(cls, v, values):
        if not 'ITEM_PIPELINES' in values.keys():
            raise ValueError("Item pipeline settings missing.")
        for key in values['ITEM_PIPELINES']:
            if not 'NLPPipeline' in key:
                continue
            else:
                assert v != None, "NLP_SETTINGS can not be null if NLPPipeline is used."
                assert v.nlp_dictionary_path.name != "", "NLP dictionary path must be defined if NLPPipeline is used."
        return v
    
    @validator('SYNONYM_SETTINGS')
    def synonym_settings(cls, v, values):
        if not 'ITEM_PIPELINES' in values.keys():
            raise ValueError("Item pipeline settings missing.")
        for key in values['ITEM_PIPELINES']:
            if not 'SynonymGatheringPipeline' in key:
                continue
            else:
                assert v != None, "SYNONYM_SETTINGS can not be null if SynonymGatheringPipeline is used."
                assert v.filepath.name != "", "Synonym file path must be defined if SynonymGatheringPipeline is used."
        return v

    @validator('CONTENT_TYPES_AND_THEMES')
    def display_fields_are_scraped(cls, v, values):
        scraper_settings = values['SCRAPER_SETTINGS'] if 'SCRAPER_SETTINGS' in values.keys() else None
        head = scraper_settings.head if scraper_settings and scraper_settings.head else None
        head_content = head.content_to_scrape if head else None
        body = scraper_settings.body if scraper_settings and scraper_settings.body else None
        body_content = body.content_to_scrape if body else None

        # Fields scraped by default
        fields_to_scrape = ['url', 'hash', 'content_type', 'themes', 'title', 'full_content']
        # Fields defined by the user appended to the default list
        if head_content:
            for item in head_content:
                fields_to_scrape.append(item)
        if body_content:
            for item in body_content:
                fields_to_scrape.append(item)
        
        display_fields = v.settings.display_fields
        for display_field in display_fields.values():
            index_fields = display_field.index_fields
            if index_fields and len(index_fields) > 0:
                for field in index_fields:
                    assert field in fields_to_scrape, f"Field '{field}' not defined in content to scrape."
        return v

class LinkExtractorRulesConfig(BaseModel):
    allow: Union[constr(min_length=1), List[constr(min_length=1)], None]
    deny: Union[constr(min_length=1), List[constr(min_length=1)], None]

class SpiderConfig(BaseModel):
    BOT_NAME: constr(min_length=1)
    ALLOWED_DOMAINS: conlist(constr(min_length=1), min_items=1)
    START_URLS: conlist(constr(min_length=1), min_items=1)
    LINK_EXTRACTOR_RULES: LinkExtractorRulesConfig
    CUSTOM_SETTINGS: CustomSettingsConfig

class GeneralConfig(BaseModel):
    DEPTH_LIMIT: Optional[int]
    DOWNLOAD_DELAY: Optional[Union[int, float]]
    DOWNLOAD_TIMEOUT: Optional[int]
    LOG_ENABLED: Optional[bool]
    LOG_FILE: Optional[Union[str, None]]
    LOG_FORMAT: Optional[str]
    LOG_LEVEL: Optional[Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']]
    LOGSTATS_INTERVAL: Optional[int]
    ROBOTSTXT_OBEY: Optional[bool]

class ScrapySettingsConfig(BaseModel):
    GENERAL: GeneralConfig
    SPIDERS: Dict[str, SpiderConfig]
# END: Scrapy conf

class ValidationModel(BaseModel):
    backend: BackendConfig
    elasticsearch: ElasticsearchConfig
    SCRAPY_SETTINGS: ScrapySettingsConfig

class Config:
    fields = {
        'class_': 'class',
        'id_': 'id'
    }