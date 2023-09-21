# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AdidasScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Price -> convert to float
        if adapter.get('price'):
            adapter['price'] = float(adapter['price'].replace('$', ''))
        else:
            adapter['price'] = 100.0

        # Description -> remove \\n from string
        if adapter.get('description'):
            adapter['description'] = adapter['description'].replace('\\n', '')
        else:
            adapter['description'] = "No description available"

        return item
