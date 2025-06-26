# Puppeteer - Headless Chrome Node.js API

## Overview
Puppeteer is a Node.js library that provides a high-level API to control headless Chrome or Chromium browsers. While primarily for JavaScript/Node.js, it's included here as it's one of the most popular web scraping tools. Python users can use Pyppeteer, an unofficial Python port.

## Installation

### Node.js (Original)
```bash
npm install puppeteer
# or
yarn add puppeteer
```

### Python (Pyppeteer)
```bash
pip install pyppeteer
```

## Key Features
- Headless browser automation
- Generate screenshots and PDFs
- Crawl SPAs and generate pre-rendered content
- Automate form submission and UI testing
- Test Chrome Extensions
- Performance testing with Chrome DevTools

## Basic Usage (JavaScript)

### Simple Example
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({ path: 'example.png' });
  await browser.close();
})();
```

### Web Scraping Example
```javascript
const puppeteer = require('puppeteer');

async function scrapeProduct(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);

  const product = await page.evaluate(() => {
    return {
      title: document.querySelector('h1').innerText,
      price: document.querySelector('.price').innerText,
      description: document.querySelector('.description').innerText,
    };
  });

  await browser.close();
  return product;
}
```

## Python Usage (Pyppeteer)

### Basic Example
```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

### Web Scraping with Pyppeteer
```python
import asyncio
from pyppeteer import launch

async def scrape_quotes():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://quotes.toscrape.com')
    
    # Wait for content
    await page.waitForSelector('.quote')
    
    # Extract data
    quotes = await page.evaluate('''() => {
        const quotes = document.querySelectorAll('.quote');
        return Array.from(quotes).map(quote => ({
            text: quote.querySelector('.text').innerText,
            author: quote.querySelector('.author').innerText,
            tags: Array.from(quote.querySelectorAll('.tag')).map(tag => tag.innerText)
        }));
    }''')
    
    await browser.close()
    return quotes

# Run
quotes = asyncio.get_event_loop().run_until_complete(scrape_quotes())
```

## Page Interactions

### Navigation and Waiting
```javascript
// Navigate with options
await page.goto('https://example.com', {
  waitUntil: 'networkidle2',
  timeout: 30000
});

// Wait for elements
await page.waitForSelector('.dynamic-content');
await page.waitForFunction('document.querySelector(".loading").style.display === "none"');

// Navigate history
await page.goBack();
await page.goForward();
await page.reload();
```

### Element Interaction
```javascript
// Click elements
await page.click('button#submit');
await page.click('text=Submit'); // Click by text

// Type text
await page.type('input[name="email"]', 'user@example.com');
await page.type('input[name="password"]', 'password', { delay: 100 });

// Select dropdown
await page.select('select#country', 'us');

// File upload
const inputUploadHandle = await page.$('input[type=file]');
await inputUploadHandle.uploadFile('/path/to/file.pdf');
```

### Form Automation
```javascript
// Complete form example
await page.type('#firstName', 'John');
await page.type('#lastName', 'Doe');
await page.type('#email', 'john@example.com');
await page.select('#country', 'USA');
await page.click('input[type="checkbox"]');
await page.click('button[type="submit"]');

// Wait for navigation after form submission
await page.waitForNavigation();
```

## Advanced Techniques

### Handling Dynamic Content
```javascript
async function scrapeSPA() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto('https://spa-example.com');
  
  // Wait for dynamic content
  await page.waitForSelector('.products-loaded');
  
  // Scroll to load more
  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });
  
  // Wait for lazy-loaded images
  await page.waitForTimeout(2000);
  
  const products = await page.$$eval('.product', elements => 
    elements.map(el => ({
      name: el.querySelector('.name').textContent,
      price: el.querySelector('.price').textContent,
      image: el.querySelector('img').src
    }))
  );
  
  await browser.close();
  return products;
}
```

### Network Interception
```javascript
// Monitor network requests
page.on('request', request => {
  console.log('Request:', request.url());
});

page.on('response', response => {
  console.log('Response:', response.url(), response.status());
});

// Intercept and modify requests
await page.setRequestInterception(true);

page.on('request', request => {
  // Block images
  if (request.resourceType() === 'image') {
    request.abort();
  }
  // Override headers
  else {
    request.continue({
      headers: Object.assign({}, request.headers(), {
        'X-Custom-Header': 'value'
      })
    });
  }
});
```

### Taking Screenshots and PDFs
```javascript
// Full page screenshot
await page.screenshot({
  path: 'fullpage.png',
  fullPage: true
});

// Element screenshot
const element = await page.$('.header');
await element.screenshot({ path: 'header.png' });

// Generate PDF
await page.pdf({
  path: 'page.pdf',
  format: 'A4',
  printBackground: true,
  margin: {
    top: '1cm',
    right: '1cm',
    bottom: '1cm',
    left: '1cm'
  }
});
```

### Cookie Management
```javascript
// Get cookies
const cookies = await page.cookies();

// Set cookies
await page.setCookie({
  name: 'session',
  value: 'abc123',
  domain: 'example.com'
});

// Delete cookies
await page.deleteCookie({ name: 'session' });
```

### Multiple Pages/Tabs
```javascript
async function scrapeMultipleTabs() {
  const browser = await puppeteer.launch();
  
  // Create multiple pages
  const page1 = await browser.newPage();
  const page2 = await browser.newPage();
  
  // Navigate in parallel
  await Promise.all([
    page1.goto('https://example1.com'),
    page2.goto('https://example2.com')
  ]);
  
  // Handle popup windows
  page1.on('popup', async (popup) => {
    console.log('Popup opened:', await popup.url());
  });
  
  await browser.close();
}
```

## Performance and Optimization

### Launch Options
```javascript
const browser = await puppeteer.launch({
  headless: false,        // Show browser window
  slowMo: 250,           // Slow down by 250ms
  devtools: true,        // Auto-open DevTools
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--disable-gpu',
    '--window-size=1920,1080'
  ]
});
```

### Page Performance
```javascript
// Disable images and CSS for faster loading
await page.setRequestInterception(true);
page.on('request', (req) => {
  if(req.resourceType() == 'stylesheet' || req.resourceType() == 'image'){
    req.abort();
  } else {
    req.continue();
  }
});

// Get page metrics
const metrics = await page.metrics();
console.log(metrics);

// Coverage data
await page.coverage.startJSCoverage();
await page.goto('https://example.com');
const jsCoverage = await page.coverage.stopJSCoverage();
```

## Error Handling
```javascript
async function robustScraping() {
  let browser;
  try {
    browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Set timeouts
    page.setDefaultTimeout(30000);
    page.setDefaultNavigationTimeout(30000);
    
    try {
      await page.goto('https://example.com', { waitUntil: 'networkidle2' });
    } catch (error) {
      console.error('Navigation failed:', error);
      return null;
    }
    
    // Handle element not found
    try {
      await page.waitForSelector('.content', { timeout: 5000 });
    } catch (error) {
      console.error('Content not found');
      return null;
    }
    
    return await page.evaluate(() => document.title);
    
  } catch (error) {
    console.error('Scraping failed:', error);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}
```

## Debugging
```javascript
// Enable verbose logging
const browser = await puppeteer.launch({
  dumpio: true,
  headless: false,
  devtools: true
});

// Take screenshot on error
page.on('error', async (error) => {
  console.error('Page error:', error);
  await page.screenshot({ path: 'error.png' });
});

// Pause execution
await page.evaluate(() => { debugger; });

// Console logging
page.on('console', msg => console.log('PAGE LOG:', msg.text()));
```

## Best Practices

1. **Resource Management**
   ```javascript
   // Always close browser
   try {
     // scraping code
   } finally {
     await browser.close();
   }
   ```

2. **Wait Strategies**
   ```javascript
   // Wait for specific conditions
   await page.waitForSelector('.loaded');
   await page.waitForFunction(() => document.readyState === 'complete');
   ```

3. **Error Recovery**
   ```javascript
   // Retry logic
   for (let i = 0; i < 3; i++) {
     try {
       await page.goto(url);
       break;
     } catch (error) {
       console.log(`Attempt ${i + 1} failed`);
     }
   }
   ```

4. **Memory Management**
   ```javascript
   // Close unused pages
   const pages = await browser.pages();
   for (const page of pages.slice(1)) {
     await page.close();
   }
   ```

## When to Use Puppeteer
- JavaScript-heavy single-page applications
- Need for Chrome-specific features
- Screenshot and PDF generation
- Automated testing of web applications
- When you need DevTools protocol access
- Performance analysis and monitoring

## Limitations
- Only supports Chromium-based browsers
- Higher memory usage than lightweight scrapers
- Can be detected by anti-bot systems
- Slower than HTTP-based scrapers

## Resources
- [Official Documentation](https://pptr.dev/)
- [GitHub Repository](https://github.com/puppeteer/puppeteer)
- [Pyppeteer Documentation](https://pyppeteer.github.io/pyppeteer/)
- [Examples](https://github.com/puppeteer/puppeteer/tree/main/examples)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)