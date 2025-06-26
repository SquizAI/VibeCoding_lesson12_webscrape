#!/bin/bash

# Run the Instagram scraper with the specified URL
# Takes screenshots every 2 seconds for up to 60 seconds

# Change to the script directory
cd "$(dirname "$0")"

# Install dependencies if needed
if ! command -v playwright &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    playwright install
fi

# Run the scraper
echo "Starting Instagram scraper..."
python instagram_scraper.py https://www.instagram.com/reel/DLKxoz6ghd_/ --interval 2 --max-duration 60

echo "Done! Check the screenshots and transcripts directories for results."
