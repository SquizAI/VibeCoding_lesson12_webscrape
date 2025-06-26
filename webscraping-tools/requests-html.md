# Requests-HTML - Python HTML Parsing for Humans

## Overview
Requests-HTML is a Python library that combines the simplicity of Requests with the power of PyQuery and the ability to execute JavaScript through Pyppeteer. It aims to make parsing HTML as simple and intuitive as possible.

## Installation
```bash
pip install requests-html
```

Note: First run will download Chromium (~100MB) for JavaScript support.

## Key Features
- Familiar requests-style API
- Full JavaScript support
- CSS selectors and XPath support
- Automatic link discovery
- Form submission handling
- Async support
- Session persistence
- Simple API for common tasks

## Basic Usage

### Simple Example
```python
from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://example.com')

# Get page title
print(r.html.find('title', first=True).text)

# Find all links
links = r.html.links
absolute_links = r.html.absolute_links
```

### Finding Elements
```python
# CSS Selectors
# Find first matching element
title = r.html.find('h1', first=True)
print(title.text)

# Find all matching elements
all_paragraphs = r.html.find('p')
for p in all_paragraphs:
    print(p.text)

# Complex selectors
items = r.html.find('div.container > ul > li.item')

# Using attributes
link = r.html.find('a[href*="example"]', first=True)
```

### XPath Support
```python
# XPath queries
title = r.html.xpath('//title/text()', first=True)

# All matching elements
links = r.html.xpath('//a[@class="external"]')

# Get attributes
hrefs = r.html.xpath('//a/@href')
```

## JavaScript Rendering

### Render JavaScript
```python
# Render JavaScript (first time downloads Chromium)
r = session.get('https://example.com')
r.html.render()

# Now you can access JavaScript-generated content
dynamic_content = r.html.find('#dynamic-content', first=True)
```

### Advanced Rendering Options
```python
# Render with options
r.html.render(
    timeout=20,           # Maximum render time
    wait=2,              # Wait before rendering
    keep_page=True,      # Keep page open for interaction
    sleep=1,             # Sleep after initial render
    scrolldown=5,        # Number of times to scroll down
)

# Execute custom JavaScript
r.html.render(script='document.querySelector("#button").click()')

# Get JavaScript return value
result = r.html.render(script='() => { return document.title }')
print(result)
```

## Form Handling

### Submit Forms
```python
# Find and fill form
r = session.get('https://example.com/login')

# Method 1: Using form search
login_form = r.html.find('form', first=True)
form_data = {
    'username': 'myuser',
    'password': 'mypass'
}

# Submit form
r = session.post(login_form.attrs['action'], data=form_data)

# Method 2: Direct submission
r = session.post('https://example.com/login', data={
    'username': 'myuser',
    'password': 'mypass'
})
```

## Data Extraction

### Element Properties
```python
element = r.html.find('#content', first=True)

# Text content
print(element.text)           # Clean text
print(element.full_text)      # Text with whitespace
print(element.html)           # Inner HTML
print(element.attrs)          # All attributes

# Specific attributes
print(element.attrs.get('class'))
print(element.attrs.get('id'))

# Search within element
sub_elements = element.find('.sub-item')
```

### Link Extraction
```python
# All links on page
all_links = r.html.links              # Relative links
absolute_links = r.html.absolute_links # Absolute links

# Links matching pattern
pattern_links = r.html.find('a[href*="article"]')
for link in pattern_links:
    print(link.attrs['href'])

# Follow links
for link in r.html.find('a.next-page'):
    next_page = session.get(link.absolute_links.pop())
```

## Advanced Examples

### Scraping Search Results
```python
def scrape_search_results(query):
    session = HTMLSession()
    
    # Perform search
    r = session.get('https://example.com/search', params={'q': query})
    
    results = []
    for item in r.html.find('.search-result'):
        result = {
            'title': item.find('h3', first=True).text,
            'url': item.find('a', first=True).attrs['href'],
            'description': item.find('.description', first=True).text
        }
        results.append(result)
    
    return results
```

### Pagination Handling
```python
def scrape_all_pages(base_url):
    session = HTMLSession()
    all_data = []
    
    r = session.get(base_url)
    
    while True:
        # Extract data from current page
        items = r.html.find('.item')
        for item in items:
            all_data.append(item.text)
        
        # Find next page link
        next_link = r.html.find('a.next', first=True)
        if not next_link:
            break
        
        # Navigate to next page
        r = session.get(next_link.absolute_links.pop())
    
    return all_data
```

### Handling Dynamic Content
```python
def scrape_spa():
    session = HTMLSession()
    r = session.get('https://spa-example.com')
    
    # Initial render
    r.html.render(wait=2, timeout=20)
    
    # Click "Load More" button multiple times
    for i in range(3):
        r.html.render(
            script='''
                document.querySelector('.load-more').click();
            ''',
            wait=2,
            sleep=2
        )
    
    # Extract all loaded items
    items = r.html.find('.item')
    return [item.text for item in items]
```

## Async Support

### Async Sessions
```python
from requests_html import AsyncHTMLSession
import asyncio

async def fetch_async(url):
    asession = AsyncHTMLSession()
    r = await asession.get(url)
    return r

async def main():
    urls = ['https://example1.com', 'https://example2.com']
    tasks = [fetch_async(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    
    for r in responses:
        print(r.html.find('title', first=True).text)

# Run async function
asyncio.run(main())
```

### Async JavaScript Rendering
```python
async def render_async():
    asession = AsyncHTMLSession()
    r = await asession.get('https://example.com')
    await r.html.arender(wait=2, sleep=2)
    
    return r.html.find('#dynamic-content', first=True).text
```

## Session Management

### Persistent Sessions
```python
# Create session with custom headers
session = HTMLSession()
session.headers.update({
    'User-Agent': 'My Custom Bot',
    'Accept-Language': 'en-US,en;q=0.9'
})

# Cookies persist across requests
r = session.get('https://example.com/login')
# ... perform login ...
r = session.get('https://example.com/protected')  # Cookies maintained
```

### Custom Browser Args
```python
# Customize browser behavior
session = HTMLSession(
    browser_args=['--no-sandbox', '--disable-setuid-sandbox']
)
```

## Parsing Features

### Table Extraction
```python
def extract_table(html_element):
    """Extract data from HTML table"""
    rows = html_element.find('tr')
    data = []
    
    for row in rows[1:]:  # Skip header
        cells = row.find('td')
        data.append([cell.text for cell in cells])
    
    return data

# Usage
r = session.get('https://example.com/data')
table = r.html.find('table', first=True)
table_data = extract_table(table)
```

### Cleaning Text
```python
# Remove extra whitespace
element = r.html.find('.content', first=True)
clean_text = ' '.join(element.text.split())

# Get text without child elements
parent = r.html.find('.parent', first=True)
own_text = parent.text
```

## Error Handling
```python
from requests_html import HTMLSession
from requests.exceptions import RequestException

def safe_scrape(url):
    session = HTMLSession()
    
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        
        # Try to render JavaScript
        try:
            r.html.render(timeout=20)
        except Exception as e:
            print(f"Render failed: {e}")
            # Continue without JavaScript content
        
        return r.html.find('title', first=True).text
        
    except RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Best Practices

1. **Use sessions for multiple requests**
   ```python
   session = HTMLSession()
   # Reuse session for better performance
   ```

2. **Handle render timeouts**
   ```python
   try:
       r.html.render(timeout=20)
   except TimeoutError:
       # Handle timeout gracefully
   ```

3. **Close browser when done**
   ```python
   # When using keep_page=True
   await r.html.page.close()
   ```

4. **Be selective with JavaScript rendering**
   ```python
   # Only render when necessary
   if r.html.find('#dynamic-content'):
       r.html.render()
   ```

5. **Use CSS selectors efficiently**
   ```python
   # More specific selectors are faster
   r.html.find('div#specific-id', first=True)
   ```

## Common Patterns

### Download Images
```python
def download_images(url):
    session = HTMLSession()
    r = session.get(url)
    
    for img in r.html.find('img'):
        img_url = img.attrs.get('src')
        if img_url:
            # Handle relative URLs
            if not img_url.startswith('http'):
                img_url = urljoin(url, img_url)
            
            # Download image
            img_response = session.get(img_url)
            filename = os.path.basename(img_url)
            
            with open(filename, 'wb') as f:
                f.write(img_response.content)
```

### Extract Metadata
```python
def get_page_metadata(url):
    session = HTMLSession()
    r = session.get(url)
    
    metadata = {
        'title': r.html.find('title', first=True).text,
        'description': None,
        'keywords': None,
        'author': None
    }
    
    # Meta tags
    for meta in r.html.find('meta'):
        if meta.attrs.get('name') == 'description':
            metadata['description'] = meta.attrs.get('content')
        elif meta.attrs.get('name') == 'keywords':
            metadata['keywords'] = meta.attrs.get('content')
        elif meta.attrs.get('name') == 'author':
            metadata['author'] = meta.attrs.get('content')
    
    return metadata
```

## Limitations
- Chromium download required for JavaScript
- Slower than pure HTTP libraries when rendering
- Limited JavaScript debugging capabilities
- Memory usage can be high with many renders
- PyPpeteer dependency can be unstable

## When to Use Requests-HTML
- Simple to medium complexity scraping tasks
- When you like the Requests library API
- Quick prototyping
- Mixed static/dynamic content
- When you need a balance between simplicity and features

## Resources
- [GitHub Repository](https://github.com/psf/requests-html)
- [Kenneth Reitz's Site](https://kennethreitz.org/)
- [PyPI Package](https://pypi.org/project/requests-html/)
- [Requests Documentation](https://requests.readthedocs.io/)