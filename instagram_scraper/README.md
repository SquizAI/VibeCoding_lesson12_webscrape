# Instagram Reel Scraper

A tool to extract transcripts and screenshots from Instagram Reels.

## Features

- Extract captions and text from Instagram Reels
- Take screenshots at regular intervals
- Download reel videos and extract audio
- Transcribe audio using OpenAI's Whisper
- Save transcripts in JSON and text formats
- Save screenshots for later AI image analysis

## Requirements

- Python 3.7+
- Playwright
- Python-dotenv
- Pillow
- yt-dlp
- ffmpeg
- OpenAI Whisper

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:

```bash
playwright install
```

## Usage

### Basic Usage

```bash
python instagram_scraper.py https://www.instagram.com/reel/REEL_ID/
```

### Audio Extraction

```bash
python audio_transcriber.py https://www.instagram.com/reel/REEL_ID/
```

### Audio Transcription

```bash
python transcribe_audio.py audio/REEL_ID.mp3 --model base
```

### Options

- `--headless`: Run in headless mode (no visible browser)
- `--interval`: Screenshot interval in seconds (default: 2)
- `--max-duration`: Maximum duration to capture in seconds (default: 60)

### Example

```bash
python instagram_scraper.py https://www.instagram.com/reel/DLKxoz6ghd_/ --interval 3 --max-duration 90
```

## Output

- Screenshots are saved in the `screenshots/[reel_id]/` directory
- Videos are saved in the `videos/` directory
- Audio files are saved in the `audio/` directory
- Transcripts are saved in the `transcripts/` directory as JSON and text files

## Next Steps

1. Implement AI image analysis for the screenshots
2. Improve transcription accuracy with larger Whisper models
3. Add support for batch processing multiple reels
4. Implement sentiment analysis on transcripts

## Notes

- Instagram's structure changes frequently, so selectors may need updates
- Audio transcription quality depends on the chosen Whisper model
- Larger models provide better accuracy but require more processing power
- Login functionality can be added for accessing private content
- yt-dlp may need updates as Instagram changes their video delivery methods
