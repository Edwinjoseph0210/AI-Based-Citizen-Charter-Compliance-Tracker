BOT_NAME = 'charter_compliance'

SPIDER_MODULES = ['scraper']
NEWSPIDER_MODULE = 'scraper'

ITEM_PIPELINES = {
    'scraper.pipelines.CharterCompliancePipeline': 300,
}
