# Prerequirements for ScraPy:
  - Elasticsearch running in elasticsearch:9200
  - Index templates etc. created (backend container is running or search_backend/setup.py has been run separately)

## OPTIONAL: Build and run NLP Container
  If you are going to run Scrapy with NLPPipeline (see the [Crawler documentation](../docs/crawler_dokumentaatio.md#spiderin-asetukset) in finnish for details), the NLP container must be running in advance.
  
  Create and run the container for finnish:<br>
  `docker run -d --name nlp-container -p 15000:7689 turkunlp/turku-neural-parser:latest-fi-en-sv-cpu server fi_tdt parse_plaintext`
  
  Create and run the container for english:<br>
  `docker run -d --name nlp-container -p 15000:7689 turkunlp/turku-neural-parser:latest-fi-en-sv-cpu server en_ewt parse_plaintext`
  
  More details available on Turku University [NLP project site](https://turkunlp.org/Turku-neural-parser-pipeline/docker.html).

# Build
  `docker build --tag crawler:latest -f ./crawler/Dockerfile .`

# Run
  `docker run --rm --name crawler --net <the_network_name_of_elasticsearch_docker> -v <the_volume_name_of_elasticsearch_docker>:/usr/share/elasticsearch -e elastic_write_username=<username_for_elastic_write> -e elastic_write_password=<password_for_elastic_write> crawler:latest`

# Start
  `docker start crawler`
