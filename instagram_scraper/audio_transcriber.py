#!/usr/bin/env python3
"""
Instagram Audio Extractor and Transcriber

This script downloads Instagram videos, extracts the audio,
and transcribes the audio content to text.
"""

import os
import re
import json
import asyncio
import argparse
import subprocess
from pathlib import Path
from urllib.parse import urlparse


class InstagramAudioExtractor:
    def __init__(self):
        """Initialize the Instagram audio extractor."""
        self.audio_dir = Path("audio")
        self.video_dir = Path("videos")
        self.transcript_dir = Path("transcripts")
        
        # Create directories if they don't exist
        self.audio_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)
        self.transcript_dir.mkdir(exist_ok=True)
    
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
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        try:
            # Check for yt-dlp
            subprocess.run(["yt-dlp", "--version"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("yt-dlp is not installed. Installing...")
            try:
                subprocess.run(["pip", "install", "yt-dlp"], check=True)
            except subprocess.SubprocessError:
                print("Failed to install yt-dlp. Please install it manually.")
                return False
        
        try:
            # Check for ffmpeg
            subprocess.run(["ffmpeg", "-version"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("ffmpeg is not installed. Please install it manually.")
            print("On macOS: brew install ffmpeg")
            print("On Ubuntu: sudo apt-get install ffmpeg")
            return False
        
        return True
    
    def download_video(self, url):
        """Download the Instagram video.
        
        Args:
            url (str): The Instagram reel URL
            
        Returns:
            str: Path to the downloaded video file
        """
        reel_id = self.extract_reel_id(url) or "instagram_video"
        output_path = self.video_dir / f"{reel_id}.mp4"
        
        print(f"Downloading video from {url}...")
        try:
            # Use yt-dlp to download the video
            subprocess.run([
                "yt-dlp",
                "--no-warnings",
                "-o", str(output_path),
                url
            ], check=True)
            
            if output_path.exists():
                print(f"Video downloaded successfully: {output_path}")
                return str(output_path)
            else:
                print("Failed to download video")
                return None
        except subprocess.SubprocessError as e:
            print(f"Error downloading video: {e}")
            return None
    
    def extract_audio(self, video_path):
        """Extract audio from the video.
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        if not video_path or not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None
        
        video_path = Path(video_path)
        audio_path = self.audio_dir / f"{video_path.stem}.mp3"
        
        print(f"Extracting audio from {video_path}...")
        try:
            # Use ffmpeg to extract audio
            subprocess.run([
                "ffmpeg",
                "-i", str(video_path),
                "-q:a", "0",
                "-map", "a",
                "-y",  # Overwrite output file if it exists
                str(audio_path)
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if audio_path.exists():
                print(f"Audio extracted successfully: {audio_path}")
                return str(audio_path)
            else:
                print("Failed to extract audio")
                return None
        except subprocess.SubprocessError as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def transcribe_audio(self, audio_path):
        """Transcribe the audio to text.
        
        This is a placeholder function. In a real implementation,
        you would use a transcription service like Google Speech-to-Text,
        AWS Transcribe, or Whisper.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Transcription result
        """
        if not audio_path or not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return {"error": "Audio file not found"}
        
        audio_path = Path(audio_path)
        transcript_path = self.transcript_dir / f"{audio_path.stem}_transcript.json"
        
        print(f"Audio file ready for transcription: {audio_path}")
        print("To transcribe this audio, you can use:")
        print("1. OpenAI Whisper (local): whisper audio_file.mp3 --model medium")
        print("2. Google Speech-to-Text API")
        print("3. AWS Transcribe")
        print("4. Other transcription services")
        
        # Placeholder for actual transcription
        transcript = {
            "status": "ready_for_transcription",
            "audio_path": str(audio_path),
            "message": "Audio extraction successful. Use a transcription service to convert to text."
        }
        
        # Save the transcript info
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2)
        
        print(f"Transcript info saved: {transcript_path}")
        return transcript
    
    def process(self, url):
        """Process an Instagram reel: download, extract audio, and prepare for transcription.
        
        Args:
            url (str): The Instagram reel URL
            
        Returns:
            dict: Processing result
        """
        if not self.check_dependencies():
            return {"error": "Missing dependencies"}
        
        # Download the video
        video_path = self.download_video(url)
        if not video_path:
            return {"error": "Failed to download video"}
        
        # Extract audio
        audio_path = self.extract_audio(video_path)
        if not audio_path:
            return {"error": "Failed to extract audio"}
        
        # Prepare for transcription
        transcript = self.transcribe_audio(audio_path)
        
        return {
            "reel_id": self.extract_reel_id(url),
            "url": url,
            "video_path": video_path,
            "audio_path": audio_path,
            "transcript": transcript
        }


def main():
    """Main function to run the audio extractor."""
    parser = argparse.ArgumentParser(description='Instagram Audio Extractor and Transcriber')
    parser.add_argument('url', help='URL of the Instagram reel')
    
    args = parser.parse_args()
    
    extractor = InstagramAudioExtractor()
    result = extractor.process(args.url)
    
    print("\nProcessing completed!")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Reel ID: {result['reel_id']}")
        print(f"Video saved: {result['video_path']}")
        print(f"Audio saved: {result['audio_path']}")
        print(f"Transcript info: {json.dumps(result['transcript'], indent=2)}")


if __name__ == "__main__":
    main()
