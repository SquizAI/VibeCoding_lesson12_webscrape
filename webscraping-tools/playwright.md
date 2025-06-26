# Playwright - Modern Web Automation

## Overview
Playwright is a modern automation library that enables reliable end-to-end testing and web scraping for modern web apps. It supports multiple browsers (Chromium, Firefox, WebKit) and provides a high-level API to control headless or headful browsers.

## Installation
```bash
# Install Playwright
pip install playwright

# Install browsers
playwright install

# Install specific browser
playwright install chromium
```

## Key Features
- Cross-browser support (Chromium, Firefox, WebKit)
- Auto-wait for elements
- Network interception
- Multiple contexts and browser instances
- Mobile device emulation
- Automatic downloads handling
- File upload support
- Geolocation, permissions, and more
- Built-in test runner

## Basic Usage

### Simple Example
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    title = page.title()
    content = page.content()
    browser.close()
```

### Async Example
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://example.com')
        title = await page.title()
        await browser.close()

asyncio.run(main())
```

## Element Selection and Interaction

### Locators
```python
# CSS selector
page.locator('button').click()
page.locator('.class-name').fill('text')

# Text content
page.locator('text=Submit').click()
page.locator('button:has-text("Submit")').click()

# XPath
page.locator('xpath=//button[@type="submit"]').click()

# Chaining
page.locator('div').filter(has_text='Product').locator('button').click()
```

### Waiting for Elements
```python
# Auto-waiting is built-in, but you can be explicit
page.wait_for_selector('.loaded')
page.wait_for_load_state('networkidle')

# Wait for specific conditions
page.locator('.spinner').wait_for(state='hidden')
page.locator('.result').wait_for(state='visible')
```

### Form Interaction
```python
# Fill forms
page.fill('input[name="username"]', 'myuser')
page.fill('input[name="password"]', 'mypass')
page.click('button[type="submit"]')

# Select options
page.select_option('select#country', 'USA')

# Check/uncheck
page.check('input[type="checkbox"]')
page.uncheck('input[type="checkbox"]')

# File upload
page.set_input_files('input[type="file"]', 'path/to/file.pdf')
```

## Advanced Scraping Examples

### Handling Dynamic Content
```python
from playwright.sync_api import sync_playwright

def scrape_spa():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate and wait for content
        page.goto('https://example.com')
        page.wait_for_selector('.dynamic-content')
        
        # Scroll to load more content
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(2000)
        
        # Extract data
        products = page.locator('.product').all()
        data = []
        for product in products:
            data.append({
                'name': product.locator('.name').text_content(),
                'price': product.locator('.price').text_content(),
            })
        
        browser.close()
        return data
```

### Intercepting Network Requests
```python
def intercept_requests():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Log all requests
        page.on('request', lambda request: print(f'>> {request.method} {request.url}'))
        page.on('response', lambda response: print(f'<< {response.status} {response.url}'))
        
        # Block images
        page.route('**/*.{png,jpg,jpeg}', lambda route: route.abort())
        
        # Modify requests
        def handle_route(route):
            headers = route.request.headers
            headers['X-Custom-Header'] = 'value'
            route.continue_(headers=headers)
        
        page.route('**/*', handle_route)
        
        page.goto('https://example.com')
        browser.close()
```

### Handling Multiple Pages
```python
def scrape_multiple_tabs():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        
        # Open multiple pages
        pages = []
        urls = ['https://example1.com', 'https://example2.com', 'https://example3.com']
        
        for url in urls:
            page = context.new_page()
            page.goto(url)
            pages.append(page)
        
        # Process all pages
        results = []
        for page in pages:
            title = page.title()
            results.append(title)
            page.close()
        
        browser.close()
        return results
```

### Taking Screenshots
```python
def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto('https://example.com')
        
        # Full page screenshot
        page.screenshot(path='fullpage.png', full_page=True)
        
        # Element screenshot
        element = page.locator('.header')
        element.screenshot(path='header.png')
        
        # PDF generation
        page.pdf(path='page.pdf', format='A4')
        
        browser.close()
```

## Authentication and Sessions

### Saving Authentication State
```python
# Login and save state
def save_auth_state():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        # Perform login
        page.goto('https://example.com/login')
        page.fill('input[name="email"]', 'user@example.com')
        page.fill('input[name="password"]', 'password')
        page.click('button[type="submit"]')
        
        # Save storage state
        context.storage_state(path='auth.json')
        browser.close()

# Reuse authentication
def use_auth_state():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(storage_state='auth.json')
        page = context.new_page()
        
        # Already logged in
        page.goto('https://example.com/dashboard')
        browser.close()
```

## Mobile and Device Emulation
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Emulate iPhone
    iphone = p.devices['iPhone 12']
    browser = p.webkit.launch()
    context = browser.new_context(**iphone)
    page = context.new_page()
    
    page.goto('https://example.com')
    page.screenshot(path='mobile.png')
    
    browser.close()
```

## Parallel Scraping
```python
import asyncio
from playwright.async_api import async_playwright

async def scrape_page(browser, url):
    page = await browser.new_page()
    await page.goto(url)
    title = await page.title()
    await page.close()
    return {'url': url, 'title': title}

async def parallel_scraping():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        urls = [
            'https://example1.com',
            'https://example2.com',
            'https://example3.com',
        ]
        
        tasks = [scrape_page(browser, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        await browser.close()
        return results

# Run
results = asyncio.run(parallel_scraping())
```

## Error Handling
```python
from playwright.sync_api import sync_playwright, TimeoutError

def robust_scraping():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Set timeout
            page.set_default_timeout(30000)  # 30 seconds
            
            page.goto('https://example.com')
            
            # Wait with timeout
            try:
                page.wait_for_selector('.content', timeout=5000)
            except TimeoutError:
                print("Content didn't load in time")
                
            # Handle navigation errors
            try:
                page.goto('https://invalid-url-example')
            except Exception as e:
                print(f"Navigation failed: {e}")
                
        finally:
            browser.close()
```

## Configuration Options
```python
# Browser launch options
browser = p.chromium.launch(
    headless=False,  # Show browser window
    slow_mo=50,      # Slow down operations by 50ms
    devtools=True,   # Open devtools
)

# Context options
context = browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Custom User Agent',
    locale='en-US',
    timezone_id='America/New_York',
    permissions=['geolocation'],
    geolocation={'latitude': 40.7128, 'longitude': -74.0060},
    color_scheme='dark',
)

# Page options
page.set_default_timeout(30000)
page.set_default_navigation_timeout(30000)
```

## Best Practices

1. **Use context for isolation**
   ```python
   context = browser.new_context()
   # Each context has separate cookies, cache, etc.
   ```

2. **Handle dynamic content properly**
   ```python
   page.wait_for_load_state('networkidle')
   page.wait_for_selector('.dynamic-content')
   ```

3. **Reuse browser instances**
   ```python
   browser = p.chromium.launch()
   # Create multiple pages/contexts
   # Close browser when done
   ```

4. **Use locators over selectors**
   ```python
   # Good
   page.locator('.button').click()
   
   # Less preferred
   page.click('.button')
   ```

5. **Error handling**
   ```python
   try:
       page.goto(url, wait_until='networkidle')
   except TimeoutError:
       # Handle timeout
   ```

## When to Use Playwright
- Modern web apps with heavy JavaScript
- Cross-browser testing requirements
- Need for browser automation features
- Mobile web scraping
- When you need screenshots/PDFs
- Complex authentication flows
- Network interception needs

## Resources
- [Official Documentation](https://playwright.dev/python/)
- [API Reference](https://playwright.dev/python/docs/api/class-playwright)
- [GitHub Repository](https://github.com/microsoft/playwright-python)
- [Examples](https://github.com/microsoft/playwright-python/tree/main/examples)