# Beautiful Soup - Web Scraping Guide

## Overview
Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping. It creates parse trees from HTML and XML documents and provides Pythonic idioms for iterating, searching, and modifying the parse tree.

## Installation
```bash
pip install beautifulsoup4
pip install lxml  # or html.parser
```

## Key Features
- Simple and Pythonic API
- Automatic encoding detection
- Tree traversal and searching
- Integration with popular parsers (lxml, html.parser)
- Handles broken HTML gracefully

## Basic Usage

### Simple Example
```python
from bs4 import BeautifulSoup
import requests

# Fetch the page
response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'html.parser')

# Find elements
title = soup.find('title').text
all_links = soup.find_all('a')
```

### Finding Elements
```python
# By tag
soup.find('div')
soup.find_all('p')

# By class
soup.find('div', class_='content')
soup.find_all('span', {'class': 'highlight'})

# By ID
soup.find('div', id='main')

# CSS selectors
soup.select('.class-name')
soup.select('#id-name')
soup.select('div > p')
```

### Extracting Data
```python
# Get text
text = element.text
text = element.get_text(strip=True)

# Get attributes
href = link.get('href')
src = img['src']

# Navigate the tree
parent = element.parent
children = element.children
siblings = element.next_sibling
```

## Advanced Examples

### Scraping a Table
```python
table = soup.find('table', {'class': 'data-table'})
rows = table.find_all('tr')

data = []
for row in rows[1:]:  # Skip header
    cols = row.find_all('td')
    data.append([col.text.strip() for col in cols])
```

### Handling Pagination
```python
def scrape_all_pages(base_url):
    page = 1
    all_data = []
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = soup.find_all('div', class_='item')
        if not items:
            break
            
        all_data.extend(items)
        page += 1
    
    return all_data
```

### Working with Forms
```python
# Extract form data
form = soup.find('form')
inputs = form.find_all('input')

form_data = {}
for input_tag in inputs:
    name = input_tag.get('name')
    value = input_tag.get('value', '')
    if name:
        form_data[name] = value
```

## Best Practices

1. **Use appropriate parser**
   - `lxml` - Fastest, requires C dependencies
   - `html.parser` - Built-in, no dependencies
   - `xml` - For XML documents

2. **Handle errors gracefully**
   ```python
   try:
       title = soup.find('h1').text
   except AttributeError:
       title = 'No title found'
   ```

3. **Respect robots.txt**
   ```python
   from urllib.robotparser import RobotFileParser
   
   rp = RobotFileParser()
   rp.set_url("https://example.com/robots.txt")
   rp.read()
   can_fetch = rp.can_fetch("*", "https://example.com/page")
   ```

4. **Add delays between requests**
   ```python
   import time
   time.sleep(1)  # Be respectful
   ```

5. **Use session for multiple requests**
   ```python
   session = requests.Session()
   session.headers.update({'User-Agent': 'Your Bot Name'})
   ```

## Common Patterns

### Extract All Links
```python
links = []
for link in soup.find_all('a', href=True):
    absolute_url = urljoin(base_url, link['href'])
    links.append(absolute_url)
```

### Download Images
```python
import os
from urllib.parse import urljoin, urlparse

img_tags = soup.find_all('img', src=True)
for img in img_tags:
    img_url = urljoin(base_url, img['src'])
    filename = os.path.basename(urlparse(img_url).path)
    
    img_data = requests.get(img_url).content
    with open(filename, 'wb') as f:
        f.write(img_data)
```

### Clean Text Extraction
```python
# Remove script and style elements
for script in soup(["script", "style"]):
    script.decompose()

# Get clean text
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)
```

## Limitations
- Not suitable for JavaScript-heavy sites
- No built-in request handling
- Can be slow for large documents
- Requires external HTTP library

## When to Use Beautiful Soup
- Simple HTML parsing tasks
- One-time scraping projects
- When you need readable code
- Educational purposes
- Quick prototypes

## Resources
- [Official Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PyPI Package](https://pypi.org/project/beautifulsoup4/)
- [GitHub Repository](https://github.com/wention/BeautifulSoup4)