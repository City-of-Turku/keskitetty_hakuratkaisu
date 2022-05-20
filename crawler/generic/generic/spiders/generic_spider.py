from scrapy import Request, Spider
from urllib.parse import urlparse
import hashlib


class GenericSpider(Spider):

    # TODO: Move all the selector creation to the Spider instance as variables. They are constructed every time as the same!

    def _get_exclude_selectors(self, exclude_rules):
        selector_list = []

        for rule in exclude_rules.values():
            if rule and len(rule) > 0:
                exc_element = rule['element'] if 'element' in rule.keys() and rule['element'] and len(
                    rule['element'].strip()) > 0 else "*"
                exc_class = rule['class'] if 'class' in rule.keys() and rule['class'] and len(
                    rule['class'].strip()) > 0 else None
                exc_id = rule['id'] if 'id' in rule.keys() and rule['id'] and len(
                    rule['id'].strip()) > 0 else None

                if exc_element != "*" or exc_class or exc_id:
                    class_selector = f'contains(@class, "{exc_class}")' if exc_class else ""
                    id_selector = f'contains(@id, "{exc_id}")' if exc_id else ""
                    selector_operator = f' and' if exc_class and exc_id else ""

                    xpath_selector = f'ancestor-or-self::{exc_element}[{class_selector}{selector_operator}{id_selector}]'
                    selector_list.append(xpath_selector)
        
        selector_str = "ancestor-or-self::script or ancestor-or-self::noscript"

        for i, selector in enumerate(selector_list):
            selector_str = f'{selector_str} or {selector}'

        return selector_str

    def _get_image_content(self, content, item_image):
        target_element = item_image["target_element"] if "target_element" in item_image.keys() and item_image["target_element"] and len(item_image["target_element"].strip()) > 0 else "img"
        target_attributes = item_image["target_attributes"] if "target_attributes" in item_image.keys() and item_image["target_attributes"] and len(item_image["target_attributes"]) > 0 else None
        content_attr = item_image["content_attribute"] if "content_attribute" in item_image.keys() and item_image["content_attribute"] and len(item_image["content_attribute"].strip()) > 0 else "src"
        alt_text_attr = item_image["alt_text"] if "alt_text" in item_image.keys() and item_image["alt_text"] and len(item_image["alt_text"]) > 0 else "alt"
        image_title_attr = item_image["title"] if "title" in item_image.keys() and item_image["title"] and len(item_image["title"]) > 0 else None

        attribute_str = ""
        if target_attributes:
            for attribute_name, attribute_value in target_attributes.items():
                if attribute_value and len(attribute_value.strip()) > 0:
                    attribute_str += f'[contains(@{attribute_name}, "{attribute_value}")]'
            attribute_str += '::' if len(attribute_str) > 0 else ""

        target_selector = content.xpath(f'descendant-or-self::{target_element}{attribute_str}')

        result = []
        
        for attribute in content_attr, alt_text_attr, image_title_attr:
            value = target_selector.xpath(f'self::*/@{attribute}').get() if attribute else None
            if value:
                result.append(value)
            else:
                result.append("")
        
        return result

    def _get_source_content(self, response, source):

        source_content = None

        src_element = source['element'] if source['element'] and len(
            source['element'].strip()) > 0 else "*"
        src_class = source['class'] if source['class'] and len(
            source['class'].strip()) > 0 else None
        src_id = source['id'] if source['id'] and len(
            source['id'].strip()) > 0 else None

        class_selector = f' contains(@class, "{src_class}")' if src_class else ""
        id_selector = f' contains(@id, "{src_id}")' if src_id else ""

        selector_constraints = f'{class_selector}{" and" if src_class else ""}{id_selector}{" and" if src_id else ""}'
        ancestor_constraints = f'{"[" if src_class or src_id else ""}{class_selector}{" and" if src_class and src_id else ""}{id_selector}{"]" if src_class or src_id else ""}'
        
        x_path_selector = f'descendant-or-self::{src_element}[{selector_constraints} not (ancestor::{src_element}{ancestor_constraints})]'

        source_content = response.xpath(x_path_selector)

        return source_content

    def _get_text(self, source_content, exclude_selectors=""):
        
        exclude_str = f'[not({exclude_selectors})]' if (exclude_selectors and len(exclude_selectors) > 0) else ""

        text_array = source_content.xpath(
            f'descendant-or-self::text(){exclude_str}').getall()
        text = ""

        for item in text_array:
            item_text = item.strip()

            text += f'{item_text} ' if len(item_text) > 0 else item_text

        return text

    def _scrape_body_items(self, response):
        if self.scraper_settings["body"]:
            scraper_settings = self.scraper_settings['body']
        else:
            return {}

        source = {
            "element": scraper_settings['element'] if 'element' in scraper_settings.keys() else "*",
            "class": scraper_settings['class'] if 'class' in scraper_settings.keys() else None,
            "id": scraper_settings['id'] if 'id' in scraper_settings.keys() else None,
            "exclude_rules": scraper_settings['exclude_rules'] if 'exclude_rules' in scraper_settings.keys() else None
        }

        source_content = self._get_source_content(response, source)

        exclude_selectors = self._get_exclude_selectors(source["exclude_rules"]) if source["exclude_rules"] else None

        items_to_scrape = scraper_settings['content_to_scrape']

        scraped_content = {}

        for item_name, item in items_to_scrape.items():
            content = source_content

            item_element = item["element"] if "element" in item.keys() and item["element"] and len(item["element"].strip()) > 0 else None
            item_attributes = item["attributes"] if "attributes" in item.keys() and item["attributes"] and len(item["attributes"]) > 0 else None
            item_type = item["type"] if "type" in item.keys() and item["type"] and len(item["type"].strip()) > 0 else "text"
            item_image = item["image"] if "image" in item.keys() and item["image"] and len(item["image"]) > 0 else None

            xpath_selector = f'descendant-or-self::{item_element}'

            if item_attributes:
                for attribute_name, attribute_value in item_attributes.items():
                    if attribute_value and len(attribute_value.strip()) > 0:
                        xpath_selector = f'{xpath_selector}[contains(@{attribute_name}, "{attribute_value}")]'

            if exclude_selectors:
                xpath_selector = f'{xpath_selector} [not({exclude_selectors})]'

            content = content.xpath(xpath_selector)

            if item_image:
                scraped_content[item_name] = self._get_image_content(content, item_image)
            else:
                scraped_content[item_name] = content.xpath(f'descendant-or-self::{item_type}()').getall()

        scraped_content["full_content"] = self._get_text(source_content, exclude_selectors)

        return scraped_content

    def _scrape_head_items(self, response):
        if self.scraper_settings["head"] and self.scraper_settings["head"]["content_to_scrape"]:
            items_to_scrape = self.scraper_settings["head"]["content_to_scrape"] if self.scraper_settings["head"]["content_to_scrape"] and len(
                self.scraper_settings["head"]["content_to_scrape"]) > 0 else None
        else:
            return {}

        scraped_content = {}
        
        for item_to_scrape_name, item_to_scrape in items_to_scrape.items():
            item_element = item_to_scrape['element']
            item_name = item_to_scrape['attribute']
            item_key = item_to_scrape['attribute-key']
            item_value = item_to_scrape['attribute-value']
            
            scraped_content[item_to_scrape_name] = response.xpath(f'//{item_element}[@{item_key}="{item_name}"]/@{item_value}').getall()

        return scraped_content

    def _scrape_lang(self, response):
        lang = ""
        if self.scraper_settings['lang']:
            
            lang_setting = self.scraper_settings['lang']

            if isinstance(lang_setting, str):
                lang = response.xpath(f'//{lang_setting}/@lang').get()
            elif 'url' in lang_setting.keys():
                index = lang_setting['path'] if 'path' in lang_setting.keys() and isinstance(lang_setting['path'], int) else 0
                lang = urlparse(response.url).path.split('/')[index + 1]

            if lang and len(lang) > 0 and lang.find("-") > 0:
                lang = lang[0:lang.find("-")]
            
            if lang:
                lang = lang.lower()
        
        return lang

    def _scrape_url(self, url):        
        scraped_content = {}

        parsedUrl = urlparse(url)
        scraped_content['domain_path'] = parsedUrl[1] + parsedUrl[2]
        scraped_content['url'] = url

        return scraped_content

    def _replace_characters(self, website_data):
        replace_dict = self.custom_settings['REPLACE_CHARACTERS']

        if replace_dict and len(replace_dict) > 0 and isinstance(replace_dict, dict):
            for lookup, replacement in replace_dict.items():
                blookup = lookup.encode('utf-8').replace(b'\\xa0', b'\xc2\xa0')
                breplacement = replacement.encode('utf-8')
                website_data = self._replace_chars_in_dict(website_data, blookup, breplacement)

        return website_data

    def _replace_chars_in_dict(self, data, blookup, breplacement):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = self._replace_chars_in_dict(value, blookup, breplacement)

                elif isinstance(value, list):
                    empty_indices = []
                    
                    for i, item in enumerate(value):
                        if isinstance(item, str):
                            value[i] = item.encode('utf-8').replace(blookup, breplacement).decode('utf-8')
                        if len(value[i].strip()) < 1:
                            empty_indices.insert(0, i)
                    
                    if len(empty_indices) > 0:
                        for index_num in empty_indices:
                            data[key].pop(index_num)
                    
                    data[key] = value

                elif isinstance(value, str):
                    data[key] = value.encode('utf-8').replace(blookup, breplacement).decode('utf-8').strip()

        return data

    def parse(self, response):
        links_only = False
        links_only_paths = self.custom_settings['CRAWL_LINKS_ONLY']
        url_path = urlparse(response.url)[2]

        for path in links_only_paths:
            if path in url_path:
                links_only = True
                self.logger.info(f'Crawl links only: {response.url}')

        if not links_only:
            website_data = {}
            self.scraper_settings = self.settings.get('SCRAPER_SETTINGS')

            website_data = self._scrape_url(response.url)
            website_data['head'] = self._scrape_head_items(response)
            website_data['body'] = self._scrape_body_items(response)
            website_data['lang'] = self._scrape_lang(response)

            if "REPLACE_CHARACTERS" in self.custom_settings.keys():
                website_data = self._replace_characters(website_data)

            full_content = website_data['body']['full_content']
            website_data['hash'] = hashlib.md5(
                full_content.encode(response.request.encoding)).hexdigest()

            yield website_data

        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
