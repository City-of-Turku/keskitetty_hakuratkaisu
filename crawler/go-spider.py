import utils
import spidertools

config_path = '../config.yaml'
process = None
spider_classes = None

config = utils.read_config(config_path)
process = spidertools.setup_process(config)
spider_classes = spidertools.setup_spider_classes(config)


for spider in spider_classes:
    process.crawl(spider_classes[spider])


print(f"Crawling...")
process.start()