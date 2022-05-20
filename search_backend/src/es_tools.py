from copy import deepcopy
from math import ceil


def get_index_templates(index_prefix, languages, indices_mapping_settings, analyzer_settings):
    templates = {}

    empty_mapping_properties = {
        "url": {
            "type": "keyword"
        },
        "hash": {
            "type": "keyword"
        },
        "content_type": {
            "type": "keyword"
        },
        "themes": {
            "type": "keyword"
        },
        "title": {
            "type": "keyword"
        },
        "head": {},
        "body": {},
        "suggest": {
            "type": "completion"
        }
    }

    for language in languages:
        template_name = f'{index_prefix}-{language}'

        for indexing_property, indexing_settings in indices_mapping_settings.items():
            if indexing_settings and len(indexing_settings) > 0:
                mapping_properties = empty_mapping_properties
                mapping_properties[indexing_property]['properties'] = {}

                for item_name, item_settings in indexing_settings.items():
                    if item_name not in mapping_properties[indexing_property]['properties'].keys():
                        index_type = None
                        if 'type' in item_settings.keys() and item_settings['type'] and len(item_settings['type'].strip()) > 0:
                            index_type = item_settings['type']
                        
                        index_analyzer = None
                        if index_type == "text":
                            if 'analyzer' in item_settings.keys() and item_settings['analyzer'] and len(item_settings['analyzer']) > 0:
                                if not isinstance(item_settings['analyzer'], str) and language in item_settings['analyzer'].keys() and item_settings['analyzer'][language]:
                                    if len(item_settings['analyzer'][language].strip()) > 0 and item_settings['analyzer'][language] != "default":
                                        index_analyzer = f"{language}-{item_settings['analyzer'][language]}"
                        
                            if not index_analyzer:
                                index_analyzer = "default"
                        
                        analyzer_obj = {
                            'type': index_type if index_type else "text",
                        }

                        if index_analyzer:
                            analyzer_obj['analyzer'] = index_analyzer

                        for setting_name, setting_value in item_settings.items():
                            if setting_name != "type" and setting_name != "analyzer":
                                analyzer_obj[setting_name] = setting_value

                        mapping_properties[indexing_property]['properties'][item_name] = analyzer_obj

        mapping_properties["body"]["properties"]["full_content"] = {
            "type": "text"
        }

        language_analyzer_settings = {}
        for key in analyzer_settings.keys():
            for k in analyzer_settings[key]:
                if k.startswith(language) or k == 'default':
                    if key not in language_analyzer_settings:
                        language_analyzer_settings[key] = {}
                    language_analyzer_settings[key][k] = analyzer_settings[key][k]

        templates[template_name] = {
            "index_patterns": [template_name],
            "priority": 500,
            "template": {
                "mappings": {
                    "properties": deepcopy(mapping_properties)
                },
                "settings": {
                    "analysis": language_analyzer_settings
                }
            },
            "version": 1
        }

    return templates


def get_query_template(query_field_lst, fuzziness, highlight_obj, display_field_lst, field_boosts_obj=None):
    query_field_str = _parse_query_template_objects(query_field_lst)
    highlight_str = _parse_query_template_objects(highlight_obj)
    display_field_str = _parse_query_template_objects(display_field_lst)
    field_boosts_str = _parse_field_boosts_object(field_boosts_obj) if field_boosts_obj else None

    main_query = f'"query_string": {{ "fields": [ {query_field_str} ] , "query": "query_value_str" }}'

    if field_boosts_str and len(field_boosts_str) > 0:
        query_obj = f' "query": {{"function_score": {{"query": {{{main_query}}}, "functions": [{field_boosts_str}]}}}}'
    else:
        query_obj = f' "query": {{{main_query}}}'

    full_query_str = f'{{{query_obj}, "highlight": {{"number_of_fragments": 1, "fields": {highlight_str}}}, "fields": [{display_field_str}], "_source": false, "size": size_value, "from": from_value}}'

    return f'{{}}\n{full_query_str}'


def _parse_field_boosts_object(field_boost_obj):
    field_boosts_str = ""

    for field_boost in field_boost_obj.values():
        if field_boost is None:
            continue

        if "values" in field_boost.keys():
            values = field_boost['values']
        else:
            continue
        
        values_str = ""
        
        if isinstance(values, str):
            values_str = values
        elif isinstance(values, list):
            for value in values:
                if len(values_str) > 0:
                    values_str += " OR "
                
                values_str += value

        if  "field" in field_boost.keys() and len(values_str) > 0 and "boost" in field_boost.keys():
            field = field_boost['field']
            boost = field_boost['boost'] if field_boost['boost'] and isinstance(float(field_boost['boost']), float) else 1
            
            if len(field_boosts_str) > 0:
                field_boosts_str += ", "

            field_boosts_str += f'{{"filter": {{"match": {{"{field}": "{values_str}"}} }}, "weight": {boost} }}'

    return field_boosts_str


def _parse_query_template_objects(obj_to_parse):
    value_str = ""

    if isinstance(obj_to_parse, list):
        for i, lst_value in enumerate(obj_to_parse):
            lst_value = f'"{lst_value}"'
            value_str = f'{value_str}{", " if i != 0 else ""}{lst_value}'

    elif isinstance(obj_to_parse, dict):
        for obj_key, obj_value in obj_to_parse.items():
            if len(value_str) == 0:
                value_str = value_str + '{'
            if len(value_str) > 1:
                value_str = f'{value_str}, '

            value_str = value_str + f'"{obj_key}": '

            if len(obj_value) > 0:
                for sub_obj_key, sub_obj_value in obj_value.items():
                    value_str = value_str + '{' + f'"{sub_obj_key}": '
                    if isinstance(sub_obj_value, int) or isinstance(sub_obj_value, float):
                        value_str = value_str + f'{sub_obj_value}' + '}'
                    else:
                        value_str = value_str + f'"{sub_obj_value}"' + '}'
            else:
                value_str = f'{value_str}{obj_value}'

        value_str = f'{value_str}' + '}'
    
    return value_str


def parse_analyzer_settings(analyzer_settings):
    # TODO: Check if the different setting values are valid for the defined setting

    analysis_obj = {
        "analyzer": {
            "default": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": "lowercase"
            }
        }
    }

    for language, analyzers in analyzer_settings.items():
        if language == 'default':
            analyzer_obj = {
                "type": "custom",
                "tokenizer": analyzers['tokenizer'] if 'tokenizer' in analyzers.keys() and analyzers['tokenizer'] and len(analyzers['tokenizer']) > 0 else "standard",
                "char_filter": analyzers['char_filters'] if 'char_filters' in analyzers.keys() and analyzers['char_filters'] and len(analyzers['char_filters']) > 0 else "",
                "filter": analyzers['token_filters'] if 'token_filters' in analyzers.keys() and analyzers['token_filters'] and len(analyzers['token_filters']) > 0 else "lowercase"
            }

            analysis_obj['analyzer']['default'] = analyzer_obj

        elif analyzers:
            for analyzer_name, settings in analyzers.items():
                analyzer_name = f'{language}-{analyzer_name}'

                char_filters = settings["char_filters"] if settings and "char_filters" in settings.keys(
                ) and settings["char_filters"] and len(settings["char_filters"]) > 0 else None
                token_filters = settings["token_filters"] if settings and "token_filters" in settings.keys(
                ) and settings["token_filters"] and len(settings["token_filters"]) > 0 else None
                tokenizer = settings["tokenizer"] if settings and "tokenizer" in settings.keys(
                ) and settings["tokenizer"] and len(settings["tokenizer"]) > 0 else "standard"

                analyzer_obj = {
                    "type": "custom",
                    "tokenizer": tokenizer,
                    "char_filter": [],
                    "filter": []
                }

                # TODO: Modify to accept array of strings or objects

                filter_sets = {
                    "char_filter": char_filters,
                    "filter": token_filters
                }

                for filter_set_name, filter_set in filter_sets.items():
                    if filter_set:
                        if isinstance(filter_set, str):
                            analyzer_obj[filter_set_name] = filter_set
                        else:
                            for filter in filter_set:
                                if isinstance(filter, str):
                                    analyzer_obj[filter_set_name].append(
                                        filter)
                                else:
                                    if filter_set_name not in analysis_obj.keys():
                                        analysis_obj[filter_set_name] = {}

                                    analysis_obj[filter_set_name][f'{analyzer_name}-{filter["type"]}'] = filter

                                    analyzer_obj[filter_set_name].append(
                                        f'{analyzer_name}-{filter["type"]}')

                analysis_obj["analyzer"][analyzer_name] = analyzer_obj

    return analysis_obj


def parse_contents_to_scrape(spider_configs):
    query_field_lst = []
    highlight_obj = {}
    display_fields_lst = []

    for spider in spider_configs.values():
        for section_name, section in spider['CUSTOM_SETTINGS']['SCRAPER_SETTINGS'].items():
            if not isinstance(section, str) and 'content_to_scrape' in section.keys():
                for item_name, item in section['content_to_scrape'].items():
                    if "search" not in item.keys() or "search" in item.keys() and not item['search']:
                        continue
                    else:
                        items_search_settings = item['search'] if "search" in item.keys(
                        ) else None

                        boost_value = ""

                        if items_search_settings and "boost" in items_search_settings.keys() and items_search_settings['boost']:
                            boost_value = f"^{items_search_settings['boost']}"

                        # if item.indexing.type is not available at all, or it is keyword or text
                        appendField = True
                        if("indexing" in item.keys() and "type" in item["indexing"].keys()):
                            if(item["indexing"]["type"] != "text" and item["indexing"]["type"] != "keyword"):
                                appendField = False

                        if(appendField):
                            query_field_lst.append(
                                f'{section_name}.{item_name}{boost_value}')

                        if items_search_settings and "highlight" in items_search_settings.keys() and items_search_settings['highlight']:
                            highlight_obj[f'{section_name}.{item_name}'] = items_search_settings['highlight'] if not isinstance(
                                items_search_settings['highlight'], bool) else {}
        for fieldname in spider['CUSTOM_SETTINGS']['CONTENT_TYPES_AND_THEMES']['settings']['display_fields'].keys():
            display_fields_lst.append(fieldname)

    return query_field_lst, highlight_obj, display_fields_lst


def parse_index_template_mappings(spider_configs):
    index_mapping = {"head": {}, "body": {}}

    for spider_name, settings in spider_configs.items():
        if "CUSTOM_SETTINGS" in settings.keys() and "SCRAPER_SETTINGS" in settings["CUSTOM_SETTINGS"].keys():

            scrape_sets = {
                "head": settings["CUSTOM_SETTINGS"]["SCRAPER_SETTINGS"]["head"]["content_to_scrape"],
                "body": settings["CUSTOM_SETTINGS"]["SCRAPER_SETTINGS"]["body"]["content_to_scrape"]
            }

            for scrape_set_name, scrape_set in scrape_sets.items():
                for item_name, item_settings in scrape_set.items():
                    if "indexing" in item_settings.keys():
                        index_mapping[scrape_set_name][item_name] = item_settings["indexing"]
                        if item_settings['indexing']['type'] == "text":
                            if "analyzer" not in item_settings['indexing'].keys() or not item_settings['indexing']['analyzer'] or len(item_settings['indexing']['analyzer']) == 0:
                                index_mapping[scrape_set_name][item_name]["analyzer"] = None
                    else:
                        index_mapping[scrape_set_name][item_name] = {
                            "type": "text",
                            "analyzer": "default"
                        }

    return index_mapping


def parse_filter_string(filters):
    if not filters:
        return ""

    filter_str = ""

    for filter_key, filter_value in filters.items():
        
        
        filter_str += f' AND {filter_key}:'
        
        if isinstance(filter_value, list):
            filter_str += '('
            for i, value in enumerate(filter_value):
                value = value.replace(' ', '\ ')
                filter_str += value
                if i < len(filter_value) - 1:
                    filter_str += f' OR '
            filter_str += ')'
        elif isinstance(filter_value, str):
            filter_str += f'({filter_value})'
                
    return filter_str


def parse_post_filter_object(filters):
    if not filters:
        return ""

    filter_str = "" 

    for filter_key, filter_value in filters.items():
        if len(filter_str) != 0:
            filter_str += ", "
        filter_str = filter_str + '"term": { "' + filter_key + '": "' + filter_value + '" }'
    
    filter_str = ' "post_filter": { ' + filter_str + ' },'

    return filter_str


def parse_results(results, page_index, per_page):
    response_obj = {}

    for i, response_value in enumerate(["primary", "secondary"]):
        result = results[i]
        
        if 'error' in result:
            return {'error': result['error']['type']}

        total_count = result['hits']['total']['value']

        response = {
            "hits": result['hits']['hits'],
            "metadata": {
                "total_count": total_count,
                "page_index": page_index,
                "per_page": per_page,
                "page_number": ceil(page_index / per_page) + 1,
                "page_count": ceil(total_count / per_page),
                "first_page": 0,
                "next_page": page_index + per_page if page_index + per_page <= (total_count - 1) else False,
                "previous_page": page_index - per_page if page_index > per_page else False if page_index == 0 else 0,
                "last_page": total_count - total_count % per_page if total_count % per_page != 0 else max(total_count - per_page, 0),
                "took": result['took']
            }
        }
        
        response_obj[response_value] = response

    return response_obj


def parse_search_term_clauses(search_term):
    # Syntax for clause formatting:
    # clauses = list of search clauses
    # tuple = ("search_term_formatting", "OPERATOR") these terms are formatted inside round brackets
    # search_term_formatting (string, lowercase) = "exact" | "splitted_exact" | "prefix" | "splitted_prefix"
    # OPERATOR (string, uppercase, default="AND") = "AND" | "OR"
    # [ "search_term_formatting", ["OPERATOR"] | ("search_term_formatting", "OPERATOR") ], [ "OPERATOR" ] [, ... ] ]

    clauses = [
        ["exact", "OR", ("splitted_exact", "AND")],
        [("splitted_exact", "OR"), "OR", ("splitted_prefix", "AND"), "OR", ("splitted_prefix", "OR")]
    ]

    cases = {
        "exact": {"prefix": '\\"', "postfix": '\\"', "splitted": False},
        "splitted_exact": {"prefix": '\\"', "postfix": '\\"', "splitted": True},
        "prefix": {"prefix": '', "postfix": '*', "splitted": False},
        "splitted_prefix": {"prefix": '', "postfix": '*', "splitted": True},
    }

    regular_search_term_lst, quoted_search_term_lst, plus_search_term_lst = _get_splitted_search_terms(search_term.strip())
    full_search_term = search_term.strip().replace('"', '').replace('+', '')
    
    search_clauses = []

    for clause in clauses:
        search_clause = _get_search_clause(clause, cases, regular_search_term_lst, quoted_search_term_lst, plus_search_term_lst, full_search_term)

        search_clauses.append(search_clause)

    # This prevents duplicate results.
    for i in range(len(search_clauses)-1, 0, -1):
        if i > 1:
            for j, previous_clause in enumerate(search_clauses):
                if j < i:
                    search_clauses[i] += f' AND NOT ({previous_clause})'
        else:
            search_clauses[i] += f' AND NOT ({search_clauses[0]})'

    return search_clauses


def _get_search_clause(clause, cases, regular_search_term_lst, quoted_search_term_lst, plus_search_term_lst, full_search_term):
    search_clause = ""

    for part in clause:
        if isinstance(part, tuple):
            if len(plus_search_term_lst):
                search_clause += "( "

            search_clause += "( "

            case = cases[part[0]]
            operator = part[1] if len(part) > 1 else ' AND '

        elif isinstance(part, str):
            if part.islower():
                case = cases[part]

                if len(plus_search_term_lst):
                    search_clause += "( "

            elif part.isupper():
                search_clause += f" {part} "
                continue
        
        else:
            raise TypeError("Type of the clause part's value was not string or tuple")

        if case['splitted']:
            terms_str = ""

            if len(quoted_search_term_lst) > 0:
                for term in quoted_search_term_lst:
                    if len(terms_str) > 0:
                        terms_str += f' {operator} '
                    
                    terms_str += f'\\"{term}\\"'

            if len(regular_search_term_lst) > 0:
                for term in regular_search_term_lst:
                    if len(terms_str) > 0:
                        terms_str += f" {operator} "
                    terms_str += f"{case['prefix']}{term}{case['postfix']}"

            search_clause += f'{terms_str}'

        elif not case['splitted']:
            search_clause += f"{case['prefix']}{full_search_term}{case['postfix']}"
        
        if isinstance(part, tuple):
            search_clause += " )"

        # Add terms with plus prefix if any
        if len(plus_search_term_lst) > 0:
            plus_term_str = ""

            for term in plus_search_term_lst:
                plus_term_str += ' AND '

                if term[0] != '"':
                    plus_term_str += f"{case['prefix']}{term}{case['postfix']}"
                else:
                    unquoted_term = term.strip('"')
                    plus_term_str += f'\\"{unquoted_term}\\"'
            
            search_clause += f'{plus_term_str} )'

    return search_clause


def _get_splitted_search_terms(search_term):
    regular_search_term_lst = []
    quoted_search_term_lst = []
    plus_search_term_lst = []

    first_plus_index = search_term.find('+')

    # Pick terms with plus
    while first_plus_index > -1:
        end_of_plus_term = search_term.find(' ', first_plus_index + 1)
        end_of_plus_term = end_of_plus_term if end_of_plus_term > -1 else len(search_term)

        plus_term = search_term[first_plus_index:end_of_plus_term].strip('+')
        plus_search_term_lst.append(plus_term)

        search_term = search_term[0:first_plus_index] + search_term[end_of_plus_term + 1:len(search_term)]
        first_plus_index = search_term.find('+')


    first_quote_index = search_term.find('"')
    
    # Pick terms with quotes and split regulars
    while first_quote_index > -1:
        if first_quote_index > 0:
            prefix_terms = search_term[0:first_quote_index].strip(' ')
            regular_search_term_lst.extend(prefix_terms.split())

        second_quote_index = search_term.find('"', first_quote_index + 1)

        quoted_term = search_term[first_quote_index:second_quote_index + 1] if second_quote_index > first_quote_index else search_term[first_quote_index:-1]
        quoted_search_term_lst.append(quoted_term.strip('"'))

        search_term = search_term[second_quote_index + 1:].strip() if second_quote_index > first_quote_index and len(search_term) > second_quote_index + 1 else ""

        first_quote_index = search_term.find('"')

    if len(search_term) > 0:
        regular_search_term_lst.extend(search_term.strip().split(" "))

    return regular_search_term_lst, quoted_search_term_lst, plus_search_term_lst