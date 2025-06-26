#!/usr/bin/env python3
"""
Instagram Reel Scraper

This script extracts transcripts and screenshots from Instagram Reels.
It uses Playwright to automate browser interactions and handle dynamic content.
"""

import os
import re
import time
import json
import asyncio
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright


class InstagramScraper:
    def __init__(self, headless=False):
        """Initialize the Instagram scraper.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
        """
        # Always use visible browser for Instagram to avoid detection
        self.headless = False  # Force non-headless mode
        self.screenshot_dir = Path("screenshots")
        self.transcript_dir = Path("transcripts")
        
        # Create directories if they don't exist
        self.screenshot_dir.mkdir(exist_ok=True)
        self.transcript_dir.mkdir(exist_ok=True)
        
    async def setup(self):
        """Set up the browser and page."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=100,  # Slow down operations to appear more human-like
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu'
            ]
        )
        
        # Use a more realistic browser profile
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
            color_scheme="light",
            has_touch=False
        )
        
        # Set default timeouts
        self.context.set_default_timeout(60000)  # 60 seconds
        self.page = await self.context.new_page()
        
    async def close(self):
        """Close the browser and playwright."""
        if hasattr(self, 'browser'):
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
            
    def extract_reel_id(self, url):
        """Extract the reel ID from the URL.
        
        Args:
            url (str): The Instagram reel URL
            
        Returns:
            str: The reel ID
        """
        # Extract the reel ID from the URL path
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        # Find the part that contains 'reel'
        for i, part in enumerate(path_parts):
            if part == 'reel' or part == 'reels' or part == 'p':
                if i + 1 < len(path_parts):
                    return path_parts[i + 1]
        
        # If we can't find it in the path, try to extract from the URL
        match = re.search(r'/(reel|reels|p)/([^/]+)', parsed_url.path)
        if match:
            return match.group(2)
            
        return None
    
    async def take_screenshots(self, url, interval=2, max_duration=60):
        """Take screenshots of the reel at regular intervals.
        
        Args:
            url (str): The Instagram reel URL
            interval (int): Interval between screenshots in seconds
            max_duration (int): Maximum duration to capture in seconds
            
        Returns:
            list: Paths to the saved screenshots
        """
        reel_id = self.extract_reel_id(url) or datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_paths = []
        
        # Create a directory for this reel's screenshots
        reel_dir = self.screenshot_dir / reel_id
        reel_dir.mkdir(exist_ok=True)
        
        # Start taking screenshots
        start_time = time.time()
        screenshot_count = 0
        
        while time.time() - start_time < max_duration:
            screenshot_path = reel_dir / f"screenshot_{screenshot_count:03d}.png"
            await self.page.screenshot(path=str(screenshot_path))
            screenshot_paths.append(str(screenshot_path))
            print(f"Screenshot saved: {screenshot_path}")
            
            screenshot_count += 1
            await asyncio.sleep(interval)
            
            # Check if video has ended (this is approximate)
            try:
                # Check if the video is still playing or has controls visible
                is_playing = await self.page.evaluate("""
                    () => {
                        // Check for common video elements
                        const video = document.querySelector('video');
                        if (video) {
                            return !video.paused && !video.ended;
                        }
                        return false;
                    }
                """)
                
                if not is_playing:
                    print("Video appears to have ended")
                    break
            except Exception as e:
                print(f"Error checking video state: {e}")
        
        return screenshot_paths
    
    async def extract_transcript(self, url):
        """Extract the transcript from the Instagram reel.
        
        Args:
            url (str): The Instagram reel URL
            
        Returns:
            dict: The transcript data
        """
        reel_id = self.extract_reel_id(url) or datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Wait for captions to load (they might be in different elements)
        await self.page.wait_for_load_state("networkidle")
        
        # Try different methods to extract captions/transcript
        transcript = {}
        
        try:
            # Method 1: Look for caption/text elements
            caption_text = await self.page.evaluate("""
                () => {
                    // Try different selectors that might contain captions
                    const selectors = [
                        'div[data-visualcompletion="caption-text"]',
                        'div.caption-container',
                        'span.caption',
                        'div._a9zs',  // Instagram caption class
                        'div._a9zm',  // Another Instagram caption class
                        'div.C4VMK span',  // Older Instagram caption class
                        'article div._ae5q', // Reels caption class
                        'span[data-lexical-text="true"]' // New Instagram text class
                    ];
                    
                    for (const selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        if (elements && elements.length > 0) {
                            return Array.from(elements).map(el => el.textContent).join(' ');
                        }
                    }
                    
                    // Try to find any visible text in the post
                    const article = document.querySelector('article');
                    if (article) {
                        return article.innerText;
                    }
                    
                    return '';
                }
            """)
            
            if caption_text and caption_text.strip():
                transcript['caption'] = caption_text.strip()
        
        except Exception as e:
            print(f"Error extracting caption: {e}")
        
        try:
            # Method 2: Look for closed captions/subtitles if available
            cc_text = await self.page.evaluate("""
                () => {
                    // Try different selectors that might contain closed captions
                    const selectors = [
                        'div.closed-captions',
                        'div.subtitles-container',
                        'div._a3gq',  // Instagram CC container
                        'div[data-visualcompletion="closed-captions"]',
                        'div._9zwu' // Another potential CC class
                    ];
                    
                    for (const selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        if (elements && elements.length > 0) {
                            return Array.from(elements).map(el => el.textContent).join(' ');
                        }
                    }
                    
                    return '';
                }
            """)
            
            if cc_text and cc_text.strip():
                transcript['closed_captions'] = cc_text.strip()
        
        except Exception as e:
            print(f"Error extracting closed captions: {e}")
        
        # Save transcript to file
        transcript_path = self.transcript_dir / f"{reel_id}_transcript.json"
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
            
        print(f"Transcript saved: {transcript_path}")
        return transcript
    
    async def handle_dialogs(self):
        """Handle any dialogs that might appear (cookie notices, login prompts, etc.)"""
        try:
            # Handle cookie consent dialog
            cookie_buttons = [
                'button[contains(text(), "Accept")]',
                'button[contains(text(), "Allow")]',
                'button[contains(text(), "I Accept")]',
                'button[contains(text(), "Accept All")]',
                'button[contains(text(), "Continue")]',
                'button[contains(text(), "Close")]',
                '[aria-label="Close"]',
                '[aria-label="Cancel"]'
            ]
            
            for selector in cookie_buttons:
                try:
                    if await self.page.locator(selector).count() > 0:
                        print(f"Clicking dialog button: {selector}")
                        await self.page.locator(selector).click()
                        await self.page.wait_for_timeout(1000)
                except Exception as e:
                    print(f"Error clicking {selector}: {e}")
                    continue
            
            # Handle login prompt
            try:
                not_now_button = self.page.locator('button:has-text("Not Now")')
                if await not_now_button.count() > 0:
                    print("Clicking 'Not Now' on login prompt")
                    await not_now_button.click()
                    await self.page.wait_for_timeout(1000)
            except Exception as e:
                print(f"Error handling login prompt: {e}")
                
        except Exception as e:
            print(f"Error in handle_dialogs: {e}")
    
    async def scrape_reel(self, url, screenshot_interval=2, max_duration=60):
        """Scrape an Instagram reel for transcript and screenshots.
        
        Args:
            url (str): The Instagram reel URL
            screenshot_interval (int): Interval between screenshots in seconds
            max_duration (int): Maximum duration to capture in seconds
            
        Returns:
            dict: The scraped data
        """
        try:
            await self.setup()
            
            # Navigate to the URL
            print(f"Navigating to {url}")
            await self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print("Page loaded, waiting for content...")
            
            # Handle any dialogs that might appear
            await self.handle_dialogs()
            
            # Wait for the page to stabilize
            await self.page.wait_for_timeout(5000)
            print("Taking initial screenshot...")
            await self.page.screenshot(path="initial_page.png")
            
            # Try different selectors for video
            video_selectors = ["video", "[role=button] video", ".tWeCl video", ".EmbeddedMediaVideo"]
            video_found = False
            
            for selector in video_selectors:
                try:
                    print(f"Looking for video with selector: {selector}")
                    await self.page.wait_for_selector(selector, state="attached", timeout=10000)
                    video_found = True
                    print(f"Found video with selector: {selector}")
                    break
                except Exception:
                    print(f"Selector {selector} not found")
            
            if not video_found:
                print("Could not find video element, continuing anyway...")
            
            # Get basic metadata
            reel_id = self.extract_reel_id(url)
            print(f"Processing reel: {reel_id}")
            
            # Extract transcript
            print("Extracting transcript...")
            transcript = await self.extract_transcript(url)
            
            # Take screenshots
            print(f"Taking screenshots every {screenshot_interval} seconds (max {max_duration} seconds)...")
            screenshot_paths = await self.take_screenshots(url, screenshot_interval, max_duration)
            
            return {
                "reel_id": reel_id,
                "url": url,
                "transcript": transcript,
                "screenshots": screenshot_paths
            }
            
        except Exception as e:
            print(f"Error scraping reel: {e}")
            return {"error": str(e)}
            
        finally:
            await self.close()


async def main():
    """Main function to run the scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Instagram Reel Scraper')
    parser.add_argument('url', help='URL of the Instagram reel')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--interval', type=int, default=2, help='Screenshot interval in seconds')
    parser.add_argument('--max-duration', type=int, default=60, help='Maximum duration to capture in seconds')
    
    args = parser.parse_args()
    
    scraper = InstagramScraper(headless=args.headless)
    result = await scraper.scrape_reel(args.url, args.interval, args.max_duration)
    
    print("\nScraping completed!")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Reel ID: {result['reel_id']}")
        print(f"Transcript: {json.dumps(result['transcript'], indent=2)}")
        print(f"Screenshots: {len(result['screenshots'])} saved")


if __name__ == "__main__":
    asyncio.run(main())
