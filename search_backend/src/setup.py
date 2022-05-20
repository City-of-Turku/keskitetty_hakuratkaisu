from es import ElasticsearchClient
import os
import sys
import utils

print(f"RUNNING SETUP SCRIPT")

###############################
##           ARGS            ##
###############################
# 1. name of this file
# 2. Elastic admin username
# 3. Elastic admin password
if not (len(sys.argv) == 3):
    sys.exit("Exitting: Admin username and password arguments not provided")


# Configs
print(f"Reading configurations...")
config_path = '../../config.yaml'
config = utils.read_config(config_path)

es_config = config['elasticsearch']
indices = []
for language in es_config['languages']:
    indices.append(f'{es_config["index_prefix"]}-{language}')

# Initialize Elastic client
print(f"Initializing Elastic client...")
client = ElasticsearchClient(
    hosts=es_config['hosts'],
    http_auth=(sys.argv[1], sys.argv[2]),
    indices=indices,
    index_prefix=es_config['index_prefix'],
    default_lang=es_config['languages'][0],
    languages=es_config['languages']
)

###############################
##    ELASTICSEARCH SETUP    ##
###############################
print(f"Creating index on Elastic...")

spider_configs = config["SCRAPY_SETTINGS"]["SPIDERS"]

if not client.create_index_template(es_config['languages'], spider_configs, es_config['analyzers']):
    print(f'Index template creation failed. Using existing template or dynamic indexing.')

if not client.create_indices():
    print(f'Indices creation failed on setup.py.')
    # TODO: How this should be handled? And how then if the index exists?

###############################
## BACKEND CREDENTIALS SETUP ##
###############################
backend_elastic_role_name = es_config['index_reader_rolename']
backend_username = os.environ.get('elastic_read_username')
backend_password = os.environ.get('elastic_read_password')

roleexistsres = client.get_role(backend_elastic_role_name)
if(roleexistsres):
    print(f"Role already exists")
else:
    ###############################
    ## CREATE A ROLE FOR BACKEND ##
    ###############################
    roledata = {
        "cluster": ["cluster:monitor/main"],  # enables pinging Elastic
        "indices": [
            {
                "names": [es_config['index_prefix']+'-*'],
                "privileges": ["read"],
            }
        ]
    }
    print(f"Creating read user role...")
    roleres = client.put_role(backend_elastic_role_name, roledata)

    if not(roleres['role']['created']):
        print(f"Creating read role failed. Create role manually or use Kibana to examine existing roles.")
    else:
        ###############################
        ## CREATE A USER FOR BACKEND ##
        ###############################
        userdata = {
            "password": backend_password,
            "roles": [backend_elastic_role_name],
            "full_name": "Search backend service user"
        }
        print(f"Creating search backend service user...")
        userres = client.put_user(backend_username, userdata)

        if not(userres['created']):
            print(f"Creating read user failed. Create user manually or use Kibana to examine existing users.")

###############################
## CRAWLER CREDENTIALS SETUP ##
###############################
crawler_elastic_role_name = es_config['index_writer_rolename']
crawler_username = os.environ.get('elastic_write_username')
crawler_password = os.environ.get('elastic_write_password')

roleexistsres = client.get_role(crawler_elastic_role_name)
if(roleexistsres):
    print(f"Role already exists")
else:
    ###############################
    ## CREATE A ROLE FOR CRAWLER ##
    ###############################
    roledata = {
        "cluster": ["cluster:monitor/main"],  # enables pinging Elastic
        "indices": [
            {
                "names": [es_config['index_prefix']+'-*'],
                "privileges": ['create_index', 'index', 'read', 'view_index_metadata'],
            }
        ]
    }
    print(f"Creating crawler user role...")
    roleres = client.put_role(crawler_elastic_role_name, roledata)

    if not(roleres['role']['created']):
        print(f"Creating crawler role failed. Create role manually or use Kibana to examine existing roles.")

    ###############################
    ## CREATE A USER FOR CRAWLER ##
    ###############################
    userdata = {
        "password": crawler_password,
        "roles": [crawler_elastic_role_name],
        "full_name": "Crawler service user"
    }
    print(f"Creating crawler service user...")
    userres = client.put_user(crawler_username, userdata)

    if not(userres['created']):
        print(f"Creating crawler user failed. Create user manually or use Kibana to examine existing users.")

print(f"Setup done")
