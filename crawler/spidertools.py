from generic.generic.spiders.generic_spider import GenericSpider
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

def setup_process(config):
    process = CrawlerProcess(config['SCRAPY_SETTINGS']["GENERAL"])
    return process

def setup_spider_classes(config):
    es_config = config['elasticsearch']
    spiders = config['SCRAPY_SETTINGS']["SPIDERS"]
    
    spider_classes = {}

    # Create spider classes with settings set according to the config file SPIDERS section.
    for spider_name, spider_settings in spiders.items():
        spider_classes[spider_name] = type(spider_name, GenericSpider.__bases__, dict(GenericSpider.__dict__))
        spider_classes[spider_name].name = spider_settings["BOT_NAME"]
        spider_classes[spider_name].allowed_domains = spider_settings["ALLOWED_DOMAINS"]
        spider_classes[spider_name].start_urls = spider_settings['START_URLS']
        spider_classes[spider_name].link_extractor = LinkExtractor(
            allow=spider_settings['LINK_EXTRACTOR_RULES']['allow'],
            deny=spider_settings['LINK_EXTRACTOR_RULES']['deny']
        )
        spider_classes[spider_name].custom_settings = _get_validated_custom_settings(spider_settings["CUSTOM_SETTINGS"])
        spider_classes[spider_name].es_config = es_config
        
    return spider_classes
    
def _get_validated_custom_settings(custom_settings):
    if not "SCRAPER_SETTINGS" in custom_settings.keys():
        raise ValueError(f'Scraper settings are not defined')

    if "lang" not in custom_settings["SCRAPER_SETTINGS"].keys():
        custom_settings["SCRAPER_SETTINGS"]["lang"] = None

    if "head" not in custom_settings["SCRAPER_SETTINGS"].keys():
        custom_settings["SCRAPER_SETTINGS"]["head"] = None
    elif custom_settings["SCRAPER_SETTINGS"]["head"] and "content_to_scrape" not in custom_settings["SCRAPER_SETTINGS"]["head"].keys():
        custom_settings["SCRAPER_SETTINGS"]["head"] = None

    if "body" not in custom_settings["SCRAPER_SETTINGS"].keys():
        custom_settings["SCRAPER_SETTINGS"]["body"] = None
    elif custom_settings["SCRAPER_SETTINGS"]["body"] and "content_to_scrape" not in custom_settings["SCRAPER_SETTINGS"]["body"].keys():
        custom_settings["SCRAPER_SETTINGS"]["body"] = None
    elif custom_settings["SCRAPER_SETTINGS"]["body"]:
        for item in ["element", "class", "id", "exclude_rules"]:
            if not item in custom_settings["SCRAPER_SETTINGS"]["body"].keys():
                custom_settings["SCRAPER_SETTINGS"]["body"][item] = None

    if not 'CRAWL_LINKS_ONLY' in custom_settings.keys() or not custom_settings['CRAWL_LINKS_ONLY']:
        custom_settings['CRAWL_LINKS_ONLY'] = []
    elif isinstance(custom_settings['CRAWL_LINKS_ONLY'], list) and len(custom_settings['CRAWL_LINKS_ONLY']) < 1:
        custom_settings['CRAWL_LINKS_ONLY'] = []
    elif isinstance(custom_settings['CRAWL_LINKS_ONLY'], str) and len(custom_settings['CRAWL_LINKS_ONLY'].strip()) > 0:
        custom_settings['CRAWL_LINKS_ONLY'] = [custom_settings['CRAWL_LINKS_ONLY']]

    if not 'REPLACE_CHARACTERS' in custom_settings.keys() or not custom_settings['REPLACE_CHARACTERS']:
        custom_settings['REPLACE_CHARACTERS'] = None

    return custom_settings