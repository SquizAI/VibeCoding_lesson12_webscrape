# Selenium - Web Browser Automation

## Overview
Selenium is a powerful tool for controlling web browsers through programs and performing browser automation. It's functional for all browsers, works on all major OS and its scripts are written in various languages including Python, Java, C#, etc.

## Installation
```bash
# Install Selenium
pip install selenium

# Install WebDriver Manager (recommended)
pip install webdriver-manager
```

### WebDriver Setup
```bash
# Download drivers manually from:
# Chrome: https://chromedriver.chromium.org/
# Firefox: https://github.com/mozilla/geckodriver/releases
# Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Safari: Built-in on macOS
```

## Key Features
- Cross-browser support
- Multiple programming language bindings
- Extensive community and documentation
- Integration with testing frameworks
- Support for parallel execution
- Mobile testing through Appium
- Grid for distributed testing

## Basic Usage

### Simple Example
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create driver
driver = webdriver.Chrome()

# Navigate to page
driver.get("https://example.com")

# Find element and interact
title = driver.title
element = driver.find_element(By.TAG_NAME, "h1")
text = element.text

# Close browser
driver.quit()
```

### Using WebDriver Manager
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Automatic driver management
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://example.com")
driver.quit()
```

## Locating Elements

### By Strategies
```python
from selenium.webdriver.common.by import By

# By ID
element = driver.find_element(By.ID, "submit-button")

# By Name
element = driver.find_element(By.NAME, "username")

# By Class Name
element = driver.find_element(By.CLASS_NAME, "nav-link")

# By Tag Name
elements = driver.find_elements(By.TAG_NAME, "a")

# By Link Text
element = driver.find_element(By.LINK_TEXT, "Click Here")

# By Partial Link Text
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

# By CSS Selector
element = driver.find_element(By.CSS_SELECTOR, "#main > div.content")

# By XPath
element = driver.find_element(By.XPATH, "//div[@class='content']//p[1]")
```

### Finding Multiple Elements
```python
# Find all links
links = driver.find_elements(By.TAG_NAME, "a")

# Find all elements with class
elements = driver.find_elements(By.CLASS_NAME, "item")

# Iterate through elements
for link in links:
    print(link.get_attribute("href"))
```

## Waiting Strategies

### Implicit Wait
```python
# Wait up to 10 seconds for elements
driver.implicitly_wait(10)
```

### Explicit Wait
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for specific element
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "myElement")))

# Wait for element to be clickable
button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))

# Wait for text to be present
wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Complete"))
```

### Custom Wait Conditions
```python
class element_has_css_class(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class
    
    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False

# Use custom condition
wait = WebDriverWait(driver, 10)
element = wait.until(element_has_css_class((By.ID, "myDiv"), "complete"))
```

## Form Interaction

### Input Fields
```python
from selenium.webdriver.common.keys import Keys

# Type text
input_field = driver.find_element(By.NAME, "username")
input_field.clear()
input_field.send_keys("myusername")

# Special keys
input_field.send_keys(Keys.CONTROL, "a")  # Select all
input_field.send_keys(Keys.DELETE)         # Delete
input_field.send_keys(Keys.RETURN)         # Enter
```

### Dropdowns
```python
from selenium.webdriver.support.ui import Select

# Select by visible text
select = Select(driver.find_element(By.ID, "country"))
select.select_by_visible_text("United States")

# Select by value
select.select_by_value("us")

# Select by index
select.select_by_index(1)

# Get all options
options = select.options
for option in options:
    print(option.text)
```

### Checkboxes and Radio Buttons
```python
# Checkbox
checkbox = driver.find_element(By.ID, "agree")
if not checkbox.is_selected():
    checkbox.click()

# Radio button
radio = driver.find_element(By.CSS_SELECTOR, "input[value='option1']")
radio.click()
```

## Advanced Scraping Examples

### Handling Dynamic Content
```python
from selenium.webdriver.common.action_chains import ActionChains

def scrape_infinite_scroll():
    driver.get("https://example.com/infinite-scroll")
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.body.scrollHeight") > last_height
        )
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Extract all items
    items = driver.find_elements(By.CLASS_NAME, "item")
    return [item.text for item in items]
```

### Handling Popups and Alerts
```python
# JavaScript Alert
driver.execute_script("alert('Hello World')")
alert = driver.switch_to.alert
print(alert.text)
alert.accept()  # or alert.dismiss()

# Prompt
prompt = driver.switch_to.alert
prompt.send_keys("My answer")
prompt.accept()

# Window handles
main_window = driver.current_window_handle
driver.find_element(By.LINK_TEXT, "Open New Window").click()

# Switch to new window
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

# Close popup and switch back
driver.close()
driver.switch_to.window(main_window)
```

### Taking Screenshots
```python
# Full page screenshot
driver.save_screenshot("screenshot.png")

# Element screenshot
element = driver.find_element(By.ID, "content")
element.screenshot("element.png")

# Get screenshot as bytes
screenshot = driver.get_screenshot_as_png()
```

### Working with IFrames
```python
# Switch to iframe by index
driver.switch_to.frame(0)

# Switch to iframe by name or ID
driver.switch_to.frame("iframe_name")

# Switch to iframe by element
iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)

# Switch back to main content
driver.switch_to.default_content()
```

## Browser Options and Capabilities

### Chrome Options
```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-agent=Mozilla/5.0...")

# Disable images
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
```

### Firefox Options
```python
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.set_preference("general.useragent.override", "Mozilla/5.0...")
firefox_options.set_preference("permissions.default.image", 2)  # Disable images

driver = webdriver.Firefox(options=firefox_options)
```

## Action Chains

### Mouse Actions
```python
from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# Hover
element = driver.find_element(By.ID, "menu")
actions.move_to_element(element).perform()

# Right-click
actions.context_click(element).perform()

# Double-click
actions.double_click(element).perform()

# Drag and drop
source = driver.find_element(By.ID, "source")
target = driver.find_element(By.ID, "target")
actions.drag_and_drop(source, target).perform()

# Click and hold
actions.click_and_hold(element).perform()
actions.release().perform()
```

### Keyboard Actions
```python
# Key combinations
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

# Type in active element
actions.send_keys("Hello World").perform()
```

## Executing JavaScript
```python
# Execute JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# Return value from JavaScript
height = driver.execute_script("return document.body.scrollHeight")

# Pass arguments to JavaScript
element = driver.find_element(By.ID, "myElement")
driver.execute_script("arguments[0].style.border='3px solid red'", element)

# Async JavaScript
driver.execute_async_script("""
    var callback = arguments[arguments.length - 1];
    setTimeout(function() {
        callback('Hello from async!');
    }, 2000);
""")
```

## Cookie Management
```python
# Get all cookies
cookies = driver.get_cookies()

# Get specific cookie
cookie = driver.get_cookie("session_id")

# Add cookie
driver.add_cookie({
    "name": "my_cookie",
    "value": "cookie_value",
    "path": "/",
    "secure": False
})

# Delete cookie
driver.delete_cookie("my_cookie")

# Delete all cookies
driver.delete_all_cookies()
```

## Page Object Model Pattern
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login")
    
    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

# Usage
login_page = LoginPage(driver)
login_page.login("user@example.com", "password")
```

## Error Handling
```python
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)

try:
    element = driver.find_element(By.ID, "myElement")
    element.click()
except NoSuchElementException:
    print("Element not found")
except StaleElementReferenceException:
    # Element is no longer attached to DOM
    element = driver.find_element(By.ID, "myElement")
    element.click()
except TimeoutException:
    print("Operation timed out")
```

## Best Practices

1. **Use explicit waits**
   ```python
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
   ```

2. **Handle StaleElementReference**
   ```python
   def safe_click(driver, locator, timeout=10):
       wait = WebDriverWait(driver, timeout)
       element = wait.until(EC.element_to_be_clickable(locator))
       element.click()
   ```

3. **Clean up resources**
   ```python
   try:
       # Your scraping code
   finally:
       driver.quit()
   ```

4. **Use Page Object Model**
   - Separate page logic from test logic
   - Improves maintainability
   - Reduces code duplication

5. **Avoid hardcoded waits**
   ```python
   # Bad
   time.sleep(5)
   
   # Good
   wait.until(EC.presence_of_element_located((By.ID, "content")))
   ```

## When to Use Selenium
- Complex JavaScript-heavy websites
- When you need real browser behavior
- Form submissions with complex validation
- Testing web applications
- When other tools fail due to anti-bot measures
- Cross-browser compatibility testing

## Limitations
- Slower than HTTP-based scrapers
- Resource intensive
- Can be detected by websites
- Requires browser drivers
- More complex setup

## Resources
- [Official Documentation](https://www.selenium.dev/documentation/)
- [Python Bindings](https://selenium-python.readthedocs.io/)
- [WebDriver Specification](https://www.w3.org/TR/webdriver/)
- [Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [GitHub Repository](https://github.com/SeleniumHQ/selenium)