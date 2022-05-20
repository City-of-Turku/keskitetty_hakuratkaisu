FROM docker.elastic.co/elasticsearch/elasticsearch:7.16.3

WORKDIR /usr/share/elasticsearch

# copy the dependencies file to the working directory
COPY ./synonyms_fi.txt ./config
COPY ./synonyms_sv.txt ./config
COPY ./synonyms_en.txt ./config
COPY ./nlp_dictionary_fi.txt ./config

# default environment variables
ENV discovery.type=single-node
ENV xpack.security.enabled=true
ENV xpack.security.authc.api_key.enabled=true
ENV ES_JAVA_OPTS="-Xms1024m -Xmx1024m"
ENV ELASTIC_PASSWORD=epassu12345
