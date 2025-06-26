# Scrapy - Professional Web Scraping Framework

## Overview
Scrapy is an open-source and collaborative web crawling framework for Python. It's designed for large-scale web scraping and provides all the tools needed to extract data from websites, process them, and store them in your preferred format.

## Installation
```bash
pip install scrapy
```

## Key Features
- Built-in support for selecting and extracting data
- Asynchronous networking for fast scraping
- Auto-throttling and concurrent requests management
- Built-in support for exporting data
- Middleware support for custom processing
- Robust error handling and retry mechanisms
- Cookie and session handling
- Built-in caching support

## Project Structure
```
myproject/
    scrapy.cfg            # deploy configuration file
    myproject/            # project's Python module
        __init__.py
        items.py          # project items definition file
        middlewares.py    # project middlewares file
        pipelines.py      # project pipelines file
        settings.py       # project settings file
        spiders/          # directory for spiders
            __init__.py
            spider1.py
            spider2.py
```

## Creating a Scrapy Project
```bash
# Create new project
scrapy startproject myproject

# Generate spider
cd myproject
scrapy genspider example example.com
```

## Basic Spider Example
```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

## Selectors

### CSS Selectors
```python
# Select elements
response.css('div.quote')
response.css('span.text::text').get()
response.css('a::attr(href)').getall()

# Nested selection
for quote in response.css('div.quote'):
    text = quote.css('span.text::text').get()
    author = quote.css('small.author::text').get()
```

### XPath Selectors
```python
# Select by XPath
response.xpath('//div[@class="quote"]')
response.xpath('//span[@class="text"]/text()').get()
response.xpath('//a/@href').getall()

# Complex XPath
response.xpath('//div[@class="quote"][1]/span[@class="text"]/text()').get()
```

## Items - Data Models
```python
# items.py
import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    category = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

# Using in spider
from myproject.items import ProductItem

class ProductSpider(scrapy.Spider):
    name = 'products'
    
    def parse(self, response):
        item = ProductItem()
        item['name'] = response.css('h1::text').get()
        item['price'] = response.css('.price::text').re_first(r'[\d.]+')
        item['stock'] = response.css('.stock::text').get()
        yield item
```

## Item Pipelines
```python
# pipelines.py
class ValidationPipeline:
    def process_item(self, item, spider):
        if item.get('price'):
            item['price'] = float(item['price'])
        return item

class DatabasePipeline:
    def __init__(self):
        self.connection = sqlite3.connect('products.db')
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                name TEXT,
                price REAL,
                stock TEXT
            )
        ''')
    
    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO products (name, price, stock) 
            VALUES (?, ?, ?)
        ''', (item['name'], item['price'], item['stock']))
        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.connection.close()

# Enable in settings.py
ITEM_PIPELINES = {
    'myproject.pipelines.ValidationPipeline': 300,
    'myproject.pipelines.DatabasePipeline': 800,
}
```

## Advanced Features

### Following Links
```python
class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = ['https://blog.example.com']
    
    def parse(self, response):
        # Extract article links
        for article in response.css('article'):
            yield response.follow(
                article.css('h2 a::attr(href)').get(),
                self.parse_article
            )
        
        # Follow pagination
        yield response.follow(
            response.css('.next-page::attr(href)').get(),
            self.parse
        )
    
    def parse_article(self, response):
        yield {
            'title': response.css('h1::text').get(),
            'content': response.css('.content::text').getall(),
            'date': response.css('.date::text').get(),
        }
```

### Handling Forms and Login
```python
class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://example.com/login']
    
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'user', 'password': 'pass'},
            callback=self.after_login
        )
    
    def after_login(self, response):
        # Check login success
        if "Welcome" in response.text:
            # Continue scraping
            yield response.follow('/protected-data', self.parse_data)
```

### Custom Settings per Spider
```python
class MySpider(scrapy.Spider):
    name = 'myspider'
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'USER_AGENT': 'My Custom Bot',
    }
```

### Middleware Example
```python
# middlewares.py
class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://proxy.example.com:8000'

class RetryMiddleware:
    def process_response(self, request, response, spider):
        if response.status in [500, 503, 504]:
            return request.copy()
        return response
```

## Running Spiders

### Command Line
```bash
# Run spider
scrapy crawl quotes

# Run with specific settings
scrapy crawl quotes -s USER_AGENT='MyBot'

# Export data
scrapy crawl quotes -O quotes.json
scrapy crawl quotes -O quotes.csv
scrapy crawl quotes -O quotes.jl  # JSON Lines

# Run in shell for testing
scrapy shell 'https://quotes.toscrape.com'
```

### From Script
```python
from scrapy.crawler import CrawlerProcess
from myproject.spiders.quotes import QuotesSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'FEEDS': {
        'items.json': {
            'format': 'json',
            'overwrite': True
        },
    }
})

process.crawl(QuotesSpider)
process.start()
```

## Settings Configuration
```python
# settings.py
BOT_NAME = 'mybot'

# Obey robots.txt
ROBOTSTXT_OBEY = True

# Configure delays
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0

# Cache
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600

# User agent
USER_AGENT = 'mybot (+http://www.yourdomain.com)'
```

## Error Handling
```python
class ErrorHandlingSpider(scrapy.Spider):
    name = 'error_handling'
    
    def parse(self, response):
        try:
            data = {
                'title': response.css('h1::text').get(),
                'price': float(response.css('.price::text').re_first(r'[\d.]+'))
            }
            yield data
        except (ValueError, TypeError) as e:
            self.logger.error(f'Error parsing {response.url}: {e}')
            
    def errback(self, failure):
        self.logger.error(repr(failure))
```

## Best Practices

1. **Respect robots.txt**
   ```python
   ROBOTSTXT_OBEY = True
   ```

2. **Use Item Loaders for complex extraction**
   ```python
   from scrapy.loader import ItemLoader
   
   loader = ItemLoader(item=ProductItem(), response=response)
   loader.add_css('name', 'h1::text')
   loader.add_xpath('price', '//span[@class="price"]/text()')
   yield loader.load_item()
   ```

3. **Implement download delays**
   ```python
   DOWNLOAD_DELAY = 2
   RANDOMIZE_DOWNLOAD_DELAY = True
   ```

4. **Handle duplicates**
   ```python
   DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
   ```

5. **Monitor performance**
   ```python
   STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'
   ```

## When to Use Scrapy
- Large-scale scraping projects
- When you need concurrent/parallel scraping
- Complex crawling patterns
- Professional data extraction pipelines
- When you need middleware and extensions
- Long-running scraping jobs

## Resources
- [Official Documentation](https://docs.scrapy.org/)
- [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
- [GitHub Repository](https://github.com/scrapy/scrapy)
- [Scrapy Cloud](https://scrapinghub.com/scrapy-cloud)